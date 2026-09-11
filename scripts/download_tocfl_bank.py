#!/usr/bin/env python3
"""Download the official, freely published TOCFL practice bank.

The script intentionally limits downloads to files hosted by the official
TOCFL/SC-TOP domains and writes a CSV manifest with source URLs and hashes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
from html.parser import HTMLParser
import mimetypes
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen


SOURCE_PAGES = [
    (
        "01_題庫型模擬試題",
        "https://tocfl.edu.tw/tocfl/index.php/exam/test/page/1"
        "?pressBtn=%28%E9%A1%8C%E5%BA%AB%29",
    ),
    (
        "02_完整模擬題本",
        "https://tocfl.edu.tw/tocfl/index.php/teach/test/page/1",
    ),
    (
        "03_正式考題公開題庫",
        "https://tocfl.edu.tw/tocfl/index.php/exam/study_resources/page/7",
    ),
    (
        "04_模擬試題詳解",
        "https://tocfl.edu.tw/tocfl/index.php/exam/study_resources/page/5",
    ),
    (
        "05_口語模擬試題",
        "https://tocfl.edu.tw/tocfl/index.php/teach/test/page/37",
    ),
]

ALLOWED_HOST_SUFFIXES = ("tocfl.edu.tw", "sc-top.org.tw")
DOWNLOAD_EXTENSIONS = {
    ".pdf",
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg",
    ".mp4",
    ".zip",
    ".rar",
    ".7z",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
}
CONTENT_TYPE_EXTENSIONS = {
    "application/pdf": ".pdf",
    "application/zip": ".zip",
    "application/x-zip-compressed": ".zip",
    "application/vnd.rar": ".rar",
    "application/x-rar-compressed": ".rar",
    "audio/mpeg": ".mp3",
    "audio/mp4": ".m4a",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/ogg": ".ogg",
    "video/mp4": ".mp4",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
}
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/126 Safari/537.36 TOCFL-study-downloader/1.0"
)


class ResourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.resources: list[tuple[str, str]] = []
        self._anchor_url: str | None = None
        self._anchor_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self._anchor_url = values["href"]
            self._anchor_text = []
        if tag in {"audio", "video", "source"} and values.get("src"):
            self.resources.append((values["src"], tag))

    def handle_data(self, data: str) -> None:
        if self._anchor_url is not None:
            self._anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._anchor_url is not None:
            label = " ".join("".join(self._anchor_text).split())
            self.resources.append((self._anchor_url, label))
            self._anchor_url = None
            self._anchor_text = []


def official_host(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == suffix or host.endswith("." + suffix) for suffix in ALLOWED_HOST_SUFFIXES)


def likely_download(url: str) -> bool:
    parsed = urlparse(url)
    path_lower = parsed.path.lower()
    extension = Path(unquote(parsed.path)).suffix.lower()
    return (
        extension in DOWNLOAD_EXTENSIONS
        or "/assets/files/" in path_lower
        or "/uploads/" in path_lower
    )


def fetch_page(url: str, retries: int = 3) -> str:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=45) as response:
                raw = response.read()
                charset = response.headers.get_content_charset() or "utf-8"
                return raw.decode(charset, errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(attempt * 2)
    raise RuntimeError(f"Cannot read source page {url}: {last_error}")


def discover_resources() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    resources_by_url: dict[str, dict[str, str]] = {}
    page_results: list[dict[str, str]] = []
    for folder, page_url in SOURCE_PAGES:
        try:
            page_html = fetch_page(page_url)
            parser = ResourceParser()
            parser.feed(page_html)
            count_before = len(resources_by_url)
            for raw_url, label in parser.resources:
                # A few official speaking-test links use Windows-style
                # backslashes in their href values. Browsers normalize them,
                # so do the same before resolving the URL.
                normalized_url = html.unescape(raw_url.strip()).replace("\\", "/")
                absolute = urljoin(page_url, normalized_url)
                if not official_host(absolute) or not likely_download(absolute):
                    continue
                clean_url = absolute.split("#", 1)[0]
                record = resources_by_url.get(clean_url)
                if record is None:
                    resources_by_url[clean_url] = {
                        "category": folder,
                        "source_page": page_url,
                        "url": clean_url,
                        "label": label,
                    }
                elif page_url not in record["source_page"].split(" | "):
                    record["source_page"] += " | " + page_url
            discovered = len(resources_by_url) - count_before
            page_results.append(
                {
                    "category": folder,
                    "source_page": page_url,
                    "status": "ok",
                    "detail": f"{discovered} unique resources added",
                }
            )
        except Exception as exc:  # Keep other source pages usable.
            page_results.append(
                {
                    "category": folder,
                    "source_page": page_url,
                    "status": "error",
                    "detail": str(exc),
                }
            )
    return list(resources_by_url.values()), page_results


def sanitize_filename(value: str) -> str:
    value = unquote(value)
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = re.sub(r"\s+", " ", value).strip(" .")
    return value[:180] or "download"


def disposition_filename(value: str | None) -> str | None:
    if not value:
        return None
    utf8_match = re.search(r"filename\*=UTF-8''([^;]+)", value, re.IGNORECASE)
    if utf8_match:
        return unquote(utf8_match.group(1).strip().strip('"'))
    basic_match = re.search(r'filename="?([^";]+)"?', value, re.IGNORECASE)
    if basic_match:
        return basic_match.group(1).strip()
    return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download_one(record: dict[str, str], destination: Path, retries: int = 3) -> dict[str, str]:
    url = record["url"]
    category_dir = destination / record["category"]
    category_dir.mkdir(parents=True, exist_ok=True)
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        part_path: Path | None = None
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=90) as response:
                content_type = response.headers.get_content_type().lower()
                header_name = disposition_filename(response.headers.get("Content-Disposition"))
                url_name = Path(unquote(urlparse(response.geturl()).path)).name
                filename = sanitize_filename(header_name or url_name or record["label"])
                suffix = Path(filename).suffix.lower()
                if not suffix:
                    extension = CONTENT_TYPE_EXTENSIONS.get(content_type)
                    if not extension:
                        extension = mimetypes.guess_extension(content_type) or ""
                    filename += extension

                target = category_dir / filename
                if target.exists():
                    existing_size = target.stat().st_size
                    if existing_size > 0:
                        return {
                            **record,
                            "status": "existing",
                            "file": str(target),
                            "bytes": str(existing_size),
                            "sha256": sha256_file(target),
                            "content_type": content_type,
                            "error": "",
                        }
                part_path = target.with_name(target.name + ".part")

                digest = hashlib.sha256()
                size = 0
                with part_path.open("wb") as output:
                    while True:
                        block = response.read(1024 * 1024)
                        if not block:
                            break
                        output.write(block)
                        digest.update(block)
                        size += len(block)
                if size == 0:
                    raise RuntimeError("server returned an empty file")
                os.replace(part_path, target)

            return {
                **record,
                "status": "downloaded",
                "file": str(target),
                "bytes": str(size),
                "sha256": digest.hexdigest(),
                "content_type": content_type,
                "error": "",
            }
        except (HTTPError, URLError, TimeoutError, OSError, RuntimeError) as exc:
            last_error = exc
            if part_path and part_path.exists():
                part_path.unlink(missing_ok=True)
            if attempt < retries:
                time.sleep(attempt * 2)

    return {
        **record,
        "status": "error",
        "file": "",
        "bytes": "0",
        "sha256": "",
        "content_type": "",
        "error": str(last_error),
    }


def write_manifests(
    destination: Path,
    results: list[dict[str, str]],
    pages: list[dict[str, str]],
) -> None:
    manifest_path = destination / "manifest.csv"
    fields = [
        "status",
        "category",
        "label",
        "file",
        "bytes",
        "sha256",
        "content_type",
        "url",
        "source_page",
        "error",
    ]
    with manifest_path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)

    source_path = destination / "來源與下載狀態.txt"
    with source_path.open("w", encoding="utf-8") as stream:
        stream.write("TOCFL 官方公開題庫下載\n")
        stream.write("僅供學習與教學參考；請遵守華測會網站的版權聲明。\n\n")
        for page in pages:
            stream.write(
                f"[{page['status']}] {page['category']}\n"
                f"{page['source_page']}\n"
                f"{page['detail']}\n\n"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "destination",
        nargs="?",
        default=r"C:\Users\USER\toclf_bank",
        help="download directory",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="only print discovery and final summary",
    )
    args = parser.parse_args()
    destination = Path(args.destination).resolve()
    destination.mkdir(parents=True, exist_ok=True)

    resources, pages = discover_resources()
    print(f"Discovered {len(resources)} unique official resources.", flush=True)
    if not resources:
        write_manifests(destination, [], pages)
        print("No downloadable resources were discovered.", file=sys.stderr)
        return 2

    results: list[dict[str, str]] = []
    for index, resource in enumerate(resources, start=1):
        result = download_one(resource, destination)
        results.append(result)
        state = "OK" if result["status"] in {"downloaded", "existing"} else "ERROR"
        if not args.quiet:
            print(f"[{index}/{len(resources)}] {state} {resource['url']}", flush=True)

    write_manifests(destination, results, pages)
    downloaded = [
        item for item in results if item["status"] in {"downloaded", "existing"}
    ]
    failed = [item for item in results if item["status"] == "error"]
    total_bytes = sum(int(item["bytes"]) for item in downloaded)
    print(
        f"Completed: {len(downloaded)} files, {total_bytes} bytes, "
        f"{len(failed)} errors. Destination: {destination}",
        flush=True,
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
