# 115-1 人工智慧概論：課程資料庫與期中專案

> **課程基本資訊**  
> - **學校與學系**：元智大學 工學院 機械工程學系  
> - **授課教師**：莊凱翔 助理教授 (Prof. Kai-Hsiang Chuang)  
> - **學期**：115-1 (115學年度第1學期)  
> - **期中專題對戰**：**第 09 組（本組） VS 第 13 組 (PK 組)**  
> - **專案題目**：UCI Machine Learning Repository — **Dry Bean Dataset (乾豆資料集)**  
> - **期中簡報時間**：**2026/10/27（第八週，20分鐘口頭簡報與 PK 答辯）**  
> - **GitHub 遠端儲存庫**：[https://github.com/ian687252lin-collab/DryBean](https://github.com/ian687252lin-collab/DryBean)

---

## 📂 整理後之全域資料夾架構導覽

本資料夾已進行系統化整理、語意化分類與架構扁平化重構，所有檔案均歸類於清晰模組中：

```text
c:\Users\IAN\Desktop\人工智慧概論\
│
├── 📁 01_課程大綱與導讀作業/
│   ├── 115-1人工智慧概論+-+intro.pdf     # 課程大綱、評分標準（期中佔 25%）、進度排程
│   ├── 分組閱讀討論紀錄表_v1.docx         # 《無限機器》書籍每週小組導讀討論記錄表
│   └── 期中專題SOP流程圖_S__4849709.jpg   # 老師課堂提供之期中作業 SOP 規範流程圖
│
├── 📁 02_課堂授課投影片/ (依週次排序)
│   ├── 第01週_人工智慧概論-簡介-20260915.pptx           # 第 1 週：AI 發展史三波浪潮與基礎概念
│   ├── 第01週_人工智慧概論-課程導讀-20260915.pptx       # 第 1 週：課程簡介、資料分割與先驗觀念
│   ├── 第03週_人工智慧概論-監督式學習-決策樹與隨機森林-20260929.pptx  # 第 3 週：決策樹深度調參、隨機森林、雜訊影響
│   └── 第05週_人工智慧概論-非監督式學習-KMeans與標準化-20261013.pptx # 第 5 週：K-Means 分群、標準化尺度致命性
│
├── 📁 03_課堂範例程式庫/
│   └── my-yzu-ai-course-main/           # 老師課堂提供之完整 Python 範例程式碼庫
│       ├── supervised-learning/         # 決策樹、隨機森林、雜訊實驗範例
│       └── unsupervised-learning/       # K-Means、標準化前後對比範例
│
├── 📁 04_期中專題_DryBean/ (核心專案根目錄，無巢狀嵌套)
│   ├── 📑 MIDTERM_REPORT.md             # ⭐️ 期中專案完整正式學術/工程書面成果報告
│   ├── 🖥️ midterm_slides.html          # ⭐️ 20 分鐘互動式全螢幕簡報（含計時器/逐字稿/PK手冊/跳轉選單/列印PDF）
│   ├── 📘 期中報告_Antigravity全自動工作流程指南.md # 期中專題全自動化工作流程指南
│   ├── 📊 人工智慧概論_期中報告選題.pdf   # 第 9 組 10/13 選題 5 分鐘簡報投影片
│   ├── 📁 data/                         # 數據集目錄
│   │   ├── raw/                         # 原始下載 Dry_Bean_Dataset.xlsx 與 zip
│   │   └── processed/                   # 清洗後 CSV 與 80/20 分層標準化特徵集
│   ├── 📁 output/                       # 實驗產出目錄
│   │   ├── figures/                     # 8 大 300 DPI 高解析度圖表庫 (01 至 08)
│   │   ├── metrics_summary.json         # 核心量化總指標數據庫 (Accuracy, F1, ARI 等)
│   │   ├── supervised_metrics.json      # 監督式學習細部指標
│   │   └── unsupervised_metrics.json    # 非監督式學習細部指標
│   ├── 📁 src/                          # 自動化流水線程式碼
│   │   ├── 00_verify_env.py             # 環境驗證腳本
│   │   ├── 01_data_pipeline.py          # 資料清洗、EDA 圖表與分層切分
│   │   ├── 02_supervised_models.py      # 決策樹調參、隨機森林、特徵重要度、抗雜訊測試
│   │   ├── 03_unsupervised_models.py    # K-Means (K=7) 標準化對比、PCA 降維
│   │   └── 04_cross_evaluation.py       # 雙軌交叉驗證、混淆矩陣與總表匯出
│   ├── 📁 venv/                         # 獨立專用 Python 3.11 虛擬環境
│   └── 📄 requirements.txt              # 專案相依套件清單
│
├── 📄 CHANGELOG.md                       # 專案更新日誌 (記錄所有演進與架構重構，最新 v1.6.0)
├── 📄 ERROR_LOG.md                       # 專案報錯與修復日誌 (完整記錄排錯溯源 ERR-001~007)
└── 📄 README.md                          # 本導覽地圖文件
```

---

## ⚡ 快速指令導覽 (Quick Start)

所有指令皆可在工作區根目錄以 PowerShell 直接執行：

### 1. 驗證專案環境 (Phase 1)
```powershell
.\04_期中專題_DryBean\venv\Scripts\python.exe .\04_期中專題_DryBean\src\00_verify_env.py
```

### 2. 執行資料前處理管線 (Phase 2 - 指令一)
```powershell
.\04_期中專題_DryBean\venv\Scripts\python.exe .\04_期中專題_DryBean\src\01_data_pipeline.py
```

### 3. 執行雙軌機器學習模型與評估 (Phase 2 - 指令二)
```powershell
# 監督式學習（決策樹深度調參、隨機森林、抗雜訊實驗）
.\04_期中專題_DryBean\venv\Scripts\python.exe .\04_期中專題_DryBean\src\02_supervised_models.py

# 非監督式學習（K-Means 標準化前後對比、PCA 2D 投影）
.\04_期中專題_DryBean\venv\Scripts\python.exe .\04_期中專題_DryBean\src\03_unsupervised_models.py

# 跨軌綜合評估與指標總表匯出
.\04_期中專題_DryBean\venv\Scripts\python.exe .\04_期中專題_DryBean\src\04_cross_evaluation.py
```

---

## 🎯 期中專題成果交付物快速捷徑 (Deliverables)

- 🖥️ **20 分鐘互動式期中簡報（雙擊或以瀏覽器開啟）**：  
  👉 [`04_期中專題_DryBean/midterm_slides.html`](file:///c:/Users/IAN/Desktop/人工智慧概論/04_期中專題_DryBean/midterm_slides.html)  
  *(支援鍵盤左右鍵換頁、快捷鍵 `F` 全螢幕、`N` 講者講稿、`P` PK 攻防手冊、`T` 計時器暫停/繼續、頂部選頁跳轉選單、`Ctrl+P` 一鍵匯出 18 頁 PDF 講義)*
- 📑 **期中正式書面專題研究報告**：  
  👉 [`04_期中專題_DryBean/MIDTERM_REPORT.md`](file:///c:/Users/IAN/Desktop/人工智慧概論/04_期中專題_DryBean/MIDTERM_REPORT.md)  
  *(完整六大章節長篇論述、LaTeX 公式推導、全實驗表格、附錄對戰第 13 組 PK 攻防手冊)*
- 📘 **期中報告全自動工作流程指南**：  
  👉 [`04_期中專題_DryBean/期中報告_Antigravity全自動工作流程指南.md`](file:///c:/Users/IAN/Desktop/人工智慧概論/04_期中專題_DryBean/期中報告_Antigravity全自動工作流程指南.md)

---
*專案文件自動維護：Antigravity IDE Agentic Engine*  
*最新重構版本：v1.6.0 (2026-10-13)*
