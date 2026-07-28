# CHANGELOG.md — 里程碑與架構決策紀錄

---

## 2026-07-26

### 官網越南文版 + TOCFL C1 模擬試題上線
- `vi/index.html`：越南文首頁上線，跟英文版共用設計系統
- `vi/c1-mock-exam.html`：TOCFL C1（Band C）模擬試題頁，5 段克漏字 30 題，**自製原創題目**（非官方真題，改寫自對官方 Band C 說明 PDF 的難度/出題邏輯理解）
- 修正越南文聲調符號渲染大小不一問題：導入 Google Fonts「Be Vietnam Pro」（完整越南文字符集支援）
- 英文版首頁 Sentence Summoner 產品卡接上實際上線連結（strategy-space.leaflune.org）

### 專案檔案整理
- LL 宇宙戰略文件（`LL_Universe_MasterPlan_v1.md` 等 5 份）搬離本專案至 `matrix-manager/inbox/`——這些文件跟 xuanxuexi 對外品牌無關，留在會被部署的目錄裡是外流風險
- 7 份產品規劃 .md（課程地圖、造句對戰規格、Flashcard 商業模式等）從根目錄歸檔進 `notes/`
- 刪除 2 份重複的「漢語單詞遊戲卡造句對戰系統」文件（`v1.0.md` / `_v1.0.md`）
- `C:\Users\USER\tocfl_bank`（TOCFL 官方素材庫、554 檔）移入本專案 `tocfl_bank/`
- 建立「乾淨資料夾部署」SOP：`wrangler pages deploy .` 絕不可對 repo 根目錄直接執行，需先複製 `index.html`/`Card/`/`vi/` 到暫存資料夾再部署，避免大型素材檔超過 CF Pages 25MiB 限制、以及內部文件外流

### 定位擴充
- colombo 明確定位 XX 為完整線上中文學習平台：教材 → 評量測驗 → 應考輔助，終局輸送「中文流利 + 懂 AI 科技」人才銜接學校/企業；客群明確為英文/越南文母語者，簡繁通吃

---

## 2026-05-08

### XX 重啟與課綱設計會議
- 揭露 XX 品牌背景：為 colombo 越南女友 Xuan 量身打造的姐妹品牌（非單純 LL 子品牌）
- 確立課綱對齊 **HSK**（非 TOCFL）
- 設計 9 冊 131 章螺旋式課綱骨架：初級 3 冊 38 章／中級 3 冊 45 章／高級 3 冊 48 章
- 12 主題 × 9 級別螺旋矩陣（同主題隨級別複雜化）
- 理論依據：Bruner Spiral Curriculum + Bengio Curriculum Learning
- 詳見會議紀錄：`matrix-manager/meetings/2026-05-08-xx-revival-and-curriculum-design.md`（**課綱尚未定案**，待對齊每冊章數、AI 線織入方式等事項）
- PROJECT.md 全面對齊 LL 三軸架構與 content-engine

---

## 2026-04-05

### 文件體系建立
- 建立 `CLAUDE.md`（AI 協作規範）、`PROJECT.md`（專案架構說明）、`README.md`、`TODO.md`、`CHANGELOG.md`
- 明確規範 Gemini / Codex 分工原則與 PROJECT.md 更新 SOP

---

## 2026-04-04

### Pinyin Poker 64 卡牌圖完成
- `Card/pp64/`：64 張 XuanXuexi 版 PNG 生成完畢
- `Card/pp64_ll/`：64 張 LeafLune 版 PNG 生成完畢
- 網頁原型完成（`index.html`、`pinyinPoker64.html`、`manyMoji.html` 等）
- 從 Neocities 備份至本地（`download_neocities_folder.py`）

---

## 2026-03-29

### TOCFL 教材生成工具
- `tocfl-material-gen/` 建立，含 `download_resources.py` 與範例素材

---

## 2026-03-25

### LL 宇宙規劃文件定稿
- `LL_Universe_MasterPlan_v1.md`：宇宙總藍圖 v1
- `LL生態系架構.md`：五大平台架構與三大閉環
- `LeafLune Universe 關係架構總覽.md`：品牌 × 平台 × IP × 商品層次
- `宣學習課程地圖架構 v1.0.md`：HSK 3.0 課程骨架
- `漢語單詞遊戲卡造句對戰系統 v1.0.md`：Sentence Summoner 完整規格
- `LeafLune 卡牌桌遊產品輸出標準 v1.0.md`：卡牌出版 SOP
- `Chinese Flashcard 商業模式規劃.md`：Flashcard MVP 與三維分類系統

---

## 架構決策紀錄

### 卡牌規格採用標準撲克牌尺寸（63 × 88 mm）
決策原因：市場通用規格，印刷廠備有標準模具，成本最低，使用者熟悉。

### 64 張分成 L/S/R/W 四花色各 16 張
決策原因：對應漢語學習四大技能（聽/說/讀/寫），十六進位識別碼（0–F）天然對應，視覺分類清晰。

### 卡牌資料分為兩套（pinyinDeck.js / pinyinDeck_ds.js）
決策原因：兩套 Emoji 圖集（xuanxuexi_emoji.png vs leaflune_emoji.png），對應不同品牌輸出需求。

### Sentence Summoner 數值只用加減法 + d6 骰子
決策原因：目標用戶是學生，運算要夠簡單；只用 d6 降低道具門檻。
