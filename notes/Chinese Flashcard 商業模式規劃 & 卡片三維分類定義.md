# Chinese Flashcard 商業模式規劃（精簡版）

---

## 一、產品 & 商業模式概要

### 1. 產品定位

**核心概念：**  
以 HSK 難度為主軸，結合「生活情境」的中文 flashcard，支援多語（中＋拼音＋英，之後可加越文）。

**產品特色：**

- 有「情境」：旅遊、日常、感情、學校、工作…
- 有「結構」：每張卡都依 難度 / 領域 / 文法 標記
- 多格式輸出：
  - CSV / Excel（可匯入 Anki / Quizlet）
  - Anki 套牌
  - PDF 列印版（單字表或小卡）

---

### 2. 目標客群（長線）

1. **國際版（英文中介語）**
   - 自學中文者、準備 HSK 的學生
2. **越南版**
   - 越南學生學中文（之後由你女友協助越文）
3. **老師 / 補習班**
   - 需要現成單字卡、句型卡的華語教師

---

### 3. 產品型態（長線）

- **主題單字包（入門商品）**
  - 例：`L1 Travel – Airport & Hotel 60 Words`
- **主題組合包**
  - 例：`Travel Pack（機場＋飯店＋交通）`
- **教師版**
  - 單字卡＋例句＋簡易教案建議

（實際定價之後再調整，現階段重點是先做出第一包）

---

## 二、卡片三維分類定義

三個維度：**難度 / 領域 / 文法**

未來全部存在 Google Sheet / DB 裡，每一列一個詞 / 句。

---

### 1. 難度（Difficulty）

- `hsk_level`：HSK1, HSK2, HSK3, HSK4, HSK5, HSK6
- `internal_level`（對使用者友善的自家分級）

| internal_level | 說明          | 粗略對應 |
|----------------|---------------|----------|
| L1             | 超基礎 / 生存 | HSK1–2   |
| L2             | 初級          | HSK2–3   |
| L3             | 中級          | HSK3–4   |
| L4             | 中高          | HSK4–5   |
| L5             | 高級          | HSK5–6+  |

---

### 2. 領域 / 場景（Domain）

#### 2.1 大領域 `domain`

例：

- daily（日常）
- travel（旅遊）
- study（學習）
- work（工作）
- relationship（感情）
- shopping（購物）
- food（飲食）
- health（健康）
- digital（數位 / 社群）
- culture（節日 / 文化）

#### 2.2 細場景 `scene`

依領域細分，例如：

- travel：`airport`, `hotel`, `transport`
- relationship：`first_meeting`, `dating`, `conflict`, `comfort`

#### 2.3 溝通功能 `speech_function`

放在同一維度下，描述這句話在場景裡的用途：

- greet / ask / answer / request / apologize / thank  
- invite / refuse / comfort / praise / complain / negotiate …

---

### 3. 文法（Grammar）

#### 3.1 單位類型 `unit_type`

- `word`：單字
- `phrase`：詞組、慣用語
- `pattern`：句型 / 文法結構

#### 3.2 詞性 `pos`

- noun / verb / adj / adv / measure / pronoun / connector / particle …

#### 3.3 文法點 `grammar_point`（給 `pattern` 用）

例：

- progressing（在…呢）
- about_to（快要…了）
- simultaneous_actions（一邊 A 一邊 B）
- contrast（雖然…但是…）

#### 3.4 句型格式 `grammar_structure`

例：

- `在 + V + 呢`
- `快要 + V/Adj + 了`
- `一邊 + V₁ + 一邊 + V₂`

#### 3.5 語體 `register`

- neutral / polite / casual / formal

---

### 4. 綜合欄位示例（單列）

| 欄位              | 範例值                             |
|-------------------|------------------------------------|
| hanzi             | 一邊 A 一邊 B                      |
| pinyin            | yìbiān A yìbiān B                  |
| meaning_en        | do A and B at the same time       |
| hsk_level         | HSK3                               |
| internal_level    | L2                                 |
| domain            | daily                              |
| scene             | daily_life                         |
| speech_function   | describe                           |
| unit_type         | pattern                            |
| pos               | –                                  |
| grammar_point     | simultaneous_actions               |
| grammar_structure | 一邊 + V₁ + 一邊 + V₂               |
| register          | neutral                            |

---

## 三、一個月內的最小 MVP

> 目標：**做出一包真的能用、能分享的 flashcard**，而不是做完整宇宙。

### 1. MVP 鎖定

- **客群**：  
  英文介面、自學中文的初學者

- **產品型態**：  
  單一小主題包（數位檔）：  
  **《L1 Travel – Airport & Hotel 60 Words》**

- **難度**：  
  HSK1–2，`internal_level = L1`

- **場景**：  
  `domain = travel`  
  `scene in (airport, hotel)`

- **文法範圍**：  
  只做 **單字卡**（`unit_type = word`）  
  每張卡包含：  
  - hanzi, pinyin  
  - meaning_en  
  - 短例句（中＋英）  
  - 標記：`hsk_level`, `domain`, `scene`, `pos`

---

### 2. 一個月實作分解（簡版）

- **第 1 週：**  
  - 決定欄位（照上面精簡版）  
  - 列出機場 + 飯店約 60 個核心單字

- **第 2 週：**  
  - 替每個單字寫 meaning_en  
  - 各寫 1 句簡單例句（中＋英）  
  - 補上 `pos`、`scene` 等標記

- **第 3 週：**  
  - 匯出 CSV  
  - 做一份 Anki 套牌  
  - 排一份簡單 PDF 單字表

- **第 4 週：**  
  - 放到 Gumroad / Ko-fi（或暫時用分享連結）  
  - 找幾位學中文的人試用，聽回饋

完成後，你們就有：

- 一份正式的「第一包產品」
- 一個可複製的流程（之後換主題直接照做）

---
