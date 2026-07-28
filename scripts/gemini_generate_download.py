from __future__ import annotations

import argparse
import base64
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, BrowserContext, Locator, Page, TimeoutError, sync_playwright


GEMINI_URL = "https://gemini.google.com/app"
COMPOSER_SELECTORS = [
    'textarea[aria-label*="prompt" i]',
    'textarea[placeholder*="prompt" i]',
    'textarea',
    '[contenteditable="true"][role="textbox"]',
    '[contenteditable="true"]',
]
SEND_BUTTON_SELECTORS = [
    'button[aria-label*="send" i]',
    'button[aria-label*="submit" i]',
    'button[aria-label*="create" i]',
    'button:has-text("Send")',
    'button:has-text("Create")',
]
COOKIE_BUTTON_SELECTORS = [
    'button:has-text("Accept all")',
    'button:has-text("I agree")',
    'button:has-text("同意")',
]
LOGIN_WAIT_SECONDS = 300
GENERATION_TIMEOUT_MS = 180_000
SETTLE_SECONDS = 6


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open Gemini, submit an image prompt, wait for images, then download them."
    )
    parser.add_argument(
        "--prompt",
        help="The image prompt to send to Gemini. If omitted, the script will ask interactively.",
    )
    parser.add_argument(
        "--output-dir",
        default="gemini-downloads",
        help="Base directory for downloaded images. Default: gemini-downloads",
    )
    parser.add_argument(
        "--profile-dir",
        default="playwright-state/gemini-edge",
        help="Persistent browser profile directory. Default: playwright-state/gemini-edge",
    )
    parser.add_argument(
        "--browser-channel",
        choices=["chromium", "chrome", "msedge"],
        default="msedge",
        help="Browser channel to launch directly. Default: msedge",
    )
    parser.add_argument(
        "--cdp-url",
        help="Connect to an already-open Chrome/Edge started with --remote-debugging-port, for example http://127.0.0.1:9222",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=GENERATION_TIMEOUT_MS,
        help=f"How long to wait for images in milliseconds. Default: {GENERATION_TIMEOUT_MS}",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run headless. By default, the browser stays visible for login and debugging.",
    )
    args = parser.parse_args()
    if not args.prompt:
        try:
            args.prompt = input("Enter the Gemini image prompt: ").strip()
        except EOFError:
            args.prompt = ""
    if not args.prompt:
        parser.error("a prompt is required. Pass --prompt or enter one when prompted.")
    return args


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def click_optional_buttons(page: Page, selectors: list[str]) -> None:
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            if locator.is_visible(timeout=1500):
                locator.click(timeout=1500)
        except Exception:
            continue


def wait_for_composer(page: Page, login_wait_seconds: int = LOGIN_WAIT_SECONDS) -> Locator:
    deadline = time.time() + login_wait_seconds

    while time.time() < deadline:
        click_optional_buttons(page, COOKIE_BUTTON_SELECTORS)
        for selector in COMPOSER_SELECTORS:
            locator = page.locator(selector).first
            try:
                if locator.is_visible(timeout=1000):
                    return locator
            except Exception:
                continue
        time.sleep(1)

    raise TimeoutError(
        f"Could not find the Gemini input box within {login_wait_seconds} seconds. "
        "If Gemini asked for login, complete it in the opened browser window and try again."
    )


def fill_prompt(composer: Locator, prompt: str) -> None:
    tag_name = composer.evaluate("(el) => el.tagName.toLowerCase()")
    composer.click()
    if tag_name in {"textarea", "input"}:
        composer.fill(prompt)
        return

    composer.evaluate(
        """
        (el, value) => {
          el.focus();
          const text = el.innerText !== undefined ? "innerText" : "textContent";
          el[text] = value;
          el.dispatchEvent(new InputEvent("input", { bubbles: true, data: value, inputType: "insertText" }));
          el.dispatchEvent(new Event("change", { bubbles: true }));
        }
        """,
        prompt,
    )


def submit_prompt(page: Page, composer: Locator) -> None:
    for selector in SEND_BUTTON_SELECTORS:
        button = page.locator(selector).first
        try:
            if button.is_visible(timeout=1000) and button.is_enabled(timeout=1000):
                button.click(timeout=1500)
                return
        except Exception:
            continue

    composer.press("Enter")


def collect_candidate_images(page: Page) -> list[dict[str, Any]]:
    return page.evaluate(
        """
        () => {
          const seen = new Set();
          return Array.from(document.images)
            .map((img, index) => {
              const src = img.currentSrc || img.src || "";
              const rect = img.getBoundingClientRect();
              return {
                index,
                src,
                alt: img.alt || "",
                width: Math.round(rect.width || img.naturalWidth || 0),
                height: Math.round(rect.height || img.naturalHeight || 0),
                visible: rect.width > 0 && rect.height > 0,
              };
            })
            .filter((img) => {
              if (!img.src || seen.has(img.src)) return false;
              seen.add(img.src);
              if (!img.visible) return false;
              if (img.width < 200 || img.height < 200) return false;
              if (img.src.startsWith("data:image/gif")) return false;
              const junk = ["googlelogo", "avatar", "profile", "icon", "logo"];
              const lower = `${img.src} ${img.alt}`.toLowerCase();
              return !junk.some((word) => lower.includes(word));
            });
        }
        """
    )


def wait_for_new_images(page: Page, baseline_urls: set[str], timeout_ms: int) -> list[dict[str, Any]]:
    deadline = time.time() + (timeout_ms / 1000)
    last_seen: list[dict[str, Any]] = []
    stable_for = 0.0
    previous_count = -1

    while time.time() < deadline:
        images = [
            image
            for image in collect_candidate_images(page)
            if image["src"] not in baseline_urls
        ]
        if images:
            if len(images) == previous_count:
                stable_for += 1
            else:
                stable_for = 0
                previous_count = len(images)
            last_seen = images
            if stable_for >= SETTLE_SECONDS:
                return images
        time.sleep(1)

    if last_seen:
        return last_seen
    raise TimeoutError("Timed out waiting for Gemini to generate visible images.")


def sanitize_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
    return cleaned or "image"


def guess_extension_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return suffix
    if url.startswith("data:image/png"):
        return ".png"
    if url.startswith("data:image/jpeg"):
        return ".jpg"
    if url.startswith("data:image/webp"):
        return ".webp"
    return ".png"


def data_url_to_bytes(url: str) -> bytes:
    _, payload = url.split(",", 1)
    return base64.b64decode(payload)


def download_url(url: str, target: Path, user_agent: str) -> bool:
    if url.startswith("data:image/"):
        target.write_bytes(data_url_to_bytes(url))
        return True

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": GEMINI_URL,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            target.write_bytes(response.read())
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return False


def screenshot_fallback(page: Page, image_src: str, target: Path) -> bool:
    locator = page.locator(f'img[src="{image_src}"]').first
    try:
        locator.screenshot(path=str(target))
        return True
    except Exception:
        return False


def save_images(page: Page, images: list[dict[str, Any]], output_dir: Path) -> list[Path]:
    saved: list[Path] = []
    user_agent = page.evaluate("() => navigator.userAgent")

    for idx, image in enumerate(images, start=1):
        extension = guess_extension_from_url(image["src"])
        alt_part = sanitize_name(image.get("alt", ""))[:30]
        filename = f"{idx:02d}"
        if alt_part and alt_part != "image":
            filename += f"-{alt_part}"
        target = output_dir / f"{filename}{extension}"

        success = download_url(image["src"], target, user_agent)
        if not success:
            png_target = target.with_suffix(".png")
            success = screenshot_fallback(page, image["src"], png_target)
            target = png_target

        if success:
            saved.append(target)
        else:
            print(f"Failed to save image #{idx}: {image['src']}", file=sys.stderr)

    return saved


def build_output_dir(base_dir: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return ensure_dir(base_dir / stamp)


def connect_to_browser(playwright: Any, args: argparse.Namespace) -> tuple[BrowserContext, Browser | None]:
    if args.cdp_url:
        browser = playwright.chromium.connect_over_cdp(args.cdp_url)
        if browser.contexts:
            context = browser.contexts[0]
        else:
            context = browser.new_context(viewport={"width": 1440, "height": 1100}, accept_downloads=True)
        return context, browser

    profile_dir = ensure_dir(Path(args.profile_dir))
    if args.browser_channel == "chromium":
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=args.headless,
            accept_downloads=True,
            viewport={"width": 1440, "height": 1100},
        )
    else:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            channel=args.browser_channel,
            headless=args.headless,
            accept_downloads=True,
            viewport={"width": 1440, "height": 1100},
        )
    return context, None


def get_or_create_page(context: BrowserContext) -> Page:
    return context.pages[0] if context.pages else context.new_page()


def run(args: argparse.Namespace) -> int:
    output_root = ensure_dir(Path(args.output_dir))
    target_dir = build_output_dir(output_root)

    with sync_playwright() as playwright:
        context, browser = connect_to_browser(playwright, args)
        try:
            page = get_or_create_page(context)
            page.goto(GEMINI_URL, wait_until="domcontentloaded")
            print("Opened Gemini.")
            if args.cdp_url:
                print("Connected to your existing Chrome session over CDP.")
            else:
                print("If Google asks you to log in, complete it in the browser window.")

            composer = wait_for_composer(page)
            baseline_urls = {image["src"] for image in collect_candidate_images(page)}

            fill_prompt(composer, args.prompt)
            submit_prompt(page, composer)
            print("Prompt submitted. Waiting for generated images...")

            images = wait_for_new_images(page, baseline_urls, args.timeout_ms)
            saved_files = save_images(page, images, target_dir)

            if not saved_files:
                print("Gemini produced images, but none could be saved.", file=sys.stderr)
                return 1

            print(f"Saved {len(saved_files)} image(s) to {target_dir.resolve()}")
            for path in saved_files:
                print(path.resolve())
            return 0
        finally:
            if browser is not None:
                browser.close()
            else:
                context.close()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
