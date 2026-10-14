<div align="center">

# 國科會大專生研究計畫 AI 輔助撰寫套件

**輸入研究主題，引導選題、文獻證據核對、C802 計畫書撰寫與評審自審**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

[繁體中文](README.md) | [English](README_EN.md)

</div>

---

## 專案簡介

本套件是專為「國科會大專學生研究計畫」打造的 AI Agent Skill。只要在支援 Agent Skills 的 AI 工具（如 Claude Code、Gemini CLI、Cursor、Codex 等）中載入此套件，並輸入你的研究領域或初步構想，AI 便會依照國科會最新規範與審查重點，一步步帶你完成從選題、文獻探討、寫滿 10 頁 C802 研究計畫書主文，直到送件前自審與成果報告撰寫的全套流程。

## 解決痛點

近年國科會審查委員對「生成式 AI 罐頭計畫書」與「AI 虛構文獻」的戒心大幅提高：

- **嚴防虛構文獻學術倫理紅線**：依據國科會與各大專院校規範，AI 產出的數據與引用必須由申請者親自查核。若出現不存在的論文或假 DOI，將直接被判定為偽造資料並遭退件。
- **去除空洞 AI 罐頭感**：充滿「顯著提升」、「深度探索」等陳腔濫調、缺乏真實數據與技術架構圖的文本，容易被評審視為缺乏獨立思考能力。
- **格式與頁數規範硬傷**：C802 計畫書主文限制於 10 頁以內，超過頁數上限或欠缺甘特圖、流程圖等關鍵圖表，常導致直接扣分。

本套件導入專業評審審稿視角，內建文獻真實性核對（citation-audit）、研究缺口（Research Gap）驗證、頁數精準控制與 Mermaid 甘特圖生成，打造令評審信服的高品質計畫書。

## 核心優勢

- **真實文獻雙重稽核與 MCP 串接**：內建引用誠信模組並支援 MCP (Model Context Protocol) 串接，自動排查虛構論文，確保每篇文獻來源皆真實可查。
- **自動化排版與精算腳本**：提供 Python 腳本估算篇幅並將 Markdown 匯出為 Word；匯出後仍需以實際 PDF／Word 人工檢查頁數與跑版。
- **評審視角 7 維度自審**：對照國科會 4 大審查重點，從原創性、論證、文獻、方法、清晰度、影響力與技術正確性進行模擬打分。
- **結構化 C802 工作流**：依研究問題、證據、方法、時程與審查疑慮逐步產出，不為了湊頁數加入空泛內容。
- **研究證據台帳與階段閘門**：借鑑 `academic-research-skills` 的 human-in-the-loop 與可追溯交接設計，將外部主張固定到來源、locator、證據摘錄與驗證狀態；未驗證項目不會被悄悄寫成已證實。
- **數據圖表可追溯渲染**：AI 可依據原始 JSON/CSV 產生 HTML/JavaScript 圖表，再由 Chromium 依真實數值渲染成 PNG，避免用影像模型猜測比例，最後嵌入 Word。

## 快速開始

即使完全沒有程式背景，也能在 1 分鐘內完成載入並開始使用。

### 方式 A：複製 GitHub 專案網址（推薦）

若你使用的是 Codex、Cursor 或 Claude Code 等工具，直接在對話框輸入：

```text
請幫我載入這個 Skill repo：https://github.com/thomas950321/nstc-undergrad-grant.git
```

載入完成後，直接提出你的需求：

```text
我想申請今年度的國科會大專生計畫，我的科系是資管系，指導教授建議做「生成式 AI 在客服的應用」，請帶我從 Step 0 開始。
```

如果只有科系或模糊想法，Skill 不會直接代寫整份計畫，而會先詢問背景與限制，再提出 2～4 個研究方向讓你選擇。每次只推進一個決策：研究方向 → 研究問題 → 資料與對象 → 方法 → 文件草稿；你可以選編號、混合選項或要求重新產生方向。

### 精確數據圖表流程

對研究數據，請保留原始 JSON/CSV，讓 AI 產生 HTML/JavaScript 圖表，再交給 Chromium 依真實數值渲染，不要讓影像模型猜測比例：

```bash
python scripts/chart_from_data.py data.json chart.html
python scripts/render_html.py chart.html chart.png
python scripts/export_c802.py proposal.md proposal.docx
```

在 `proposal.md` 中使用 `![圖名](chart.png)`。匯出的 Word 會嵌入實際 PNG；原始數據欄位不一致或圖片不存在時，流程會停止並回報錯誤。

### 方式 B：手動複製技能資料夾

將下載的 `nstc-undergrad-grant` 資料夾複製至對應 AI 工具的技能目錄：

- **Claude Code**：`~/.claude/skills/nstc-undergrad-grant/`
- **Gemini CLI**：`~/.gemini/skills/nstc-undergrad-grant/`
- **Cursor / 其他工具**：放至專案根目錄 `.agents/skills/`

## 運作原理與 7 大步驟

1. **Step 0 前置檢查**：依當年度官方與校內公告確認資格、截止時間、學術倫理、經費與附件。
2. **Step 1 選題與缺口驗證**：收斂 2~3 個候選題目，比對現有方案優缺點，驗證研究缺口是否成立。
3. **Step 2 文獻回顧與證據台帳**：整理關鍵文獻矩陣，逐筆核對來源，防範 AI 幻覺。
4. **Step 3 C802 計畫書撰寫**：依摘要、動機、文獻、方法、時程與指導內容逐段撰寫，並以實際排版結果檢查頁數。
5. **Step 4 評審視角 7 維度自審**：模擬評審評分（目標 ≥28/35 分），並方針對弱項進行修改迴圈。
6. **Step 5 送件前格式檢查**：核對 12pt 標楷體/Times New Roman、1.5 倍行高、PDF 無跑版與 C801~C804 表單完整性。
7. **Step 6 成果報告撰寫**：計畫執行期滿後 1 個月內協助產出成果報告，維持創作獎評獎資格。

### 證據台帳快速檢查

先複製 `templates/evidence_ledger.json`，逐筆填入研究主張與可追溯來源，再執行：

```bash
python scripts/validate_evidence_ledger.py evidence_ledger.json
```

這個工具只檢查台帳結構、狀態與 provenance 欄位，不會假裝替你查證論文是否存在。`verified` 必須有核對日期與 locator；無法查清的項目保留 `needs-check`，並在 C802 草稿與最終交付的「待確認」清單中揭露。

## 專案結構

```
nstc-undergrad-grant/
├── SKILL.md                        # 主技能檔案：完整引導工作流程（Step 0~6）
├── mcp_config.json                 # MCP 伺服器設定檔 (防幻覺與真實文獻 API 搜尋)
├── scripts/                        # 自動化輔助腳本
│   ├── export_c802.py              # 一鍵匯出符合國科會排版規範的 Word 檔
│   ├── check_budget.py             # 估算字數與圖表是否符合 10 頁版面限制
│   ├── validate_skill.py            # 檢查 skill metadata 與資源路徑
│   ├── chart_from_data.py           # 將原始 JSON 數據產生 HTML/SVG 圖表
│   ├── render_html.py               # 用 Chromium 將 HTML 圖表渲染成 PNG
│   ├── fetch_image.py              # 下載遠端圖片供 Word 嵌入
│   ├── validate_evidence_ledger.py # 驗證證據台帳結構與 provenance 欄位
│   └── requirements.txt            # Python 腳本相依套件
├── references/
│   ├── nstc_format_rules.md        # 國科會制度、表號、格式規範與 10 大避坑清單
│   ├── section_template.md         # 摘要黃金公式與各章節詳細寫法模板
│   ├── reviewer_checklist.md       # 7 維度評審自審清單與國科會審查重點對照
│   └── research_evidence_protocol.md # 證據層級、研究護照與兩道完整性閘門
├── templates/
│   └── evidence_ledger.json        # 可驗證的主張—來源台帳範本
└── prompts/
    ├── abstract.md                 # 300 字摘要生成與 30 秒評審壓力測試 Prompt
    ├── gap_analysis.md             # 研究缺口矩陣與文獻真偽驗證 Prompt
    └── gantt.md                    # 8 個月時程 Mermaid 甘特圖 Prompt
```

## 授權條款

本專案採用 [MIT License](./LICENSE) 授權。

## 重要聲明

- 所有申請時程、法規與經費金額，請務必以國科會官網（nstc.gov.tw）當年度最新公告為準。
- 生成式 AI 僅為研究與寫作之輔助工具，請勿偽造數據或抄襲，並請依各校及各學門規定如實揭露使用情形。
- 本套件為社群開源輔助範本，非國科會官方發行文件。

## 參與貢獻

歡迎任何形式的貢獻！無論是補充最新年度的國科會規範、優化提示詞（Prompts）、修正錯字，或是提供更豐富的各學門撰寫範例，都非常歡迎提交 Pull Request 或開立 Issue，一起讓這個套件更完善。

## 資料來源

- 國科會「大專學生研究計畫」官方專區與 Q&A
- 國科會「大專學生研究計畫作業要點」（113.11.1 修正版）
- 行政院與國科會推動生成式 AI 注意事項及學術倫理指引
- wiki.interaction.tw 計畫書撰寫攻略
