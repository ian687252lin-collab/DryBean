# 專案更新日誌 (CHANGELOG)

本專案記錄元智大學《115-1 人工智慧概論》期中專題（第 9 組 vs 第 13 組：UCI Dry Bean 乾豆資料集）之工作進程、檔案重構與自動化管線演進。

---

## [v1.6.0] - 2026-10-13 (目前版本)
### 🗂️ 全域檔案二次深度整理、分類優化與目錄架構扁平化 (Global Reorganization & Consolidation)
- **期中專案目錄扁平化 (Zero-Nesting Consolidation)**：
  - 徹底消除原本巢狀嵌套之 `midterm_drybean/` 目錄，將 `src/`、`data/`、`output/`、`venv/`、`requirements.txt` 全數提升至 `04_期中專題_DryBean/` 主目錄。
  - 移除暫時性目錄交聯點 (Directory Junction)，使所有資料夾與圖表原生直通，根絕路徑衝突。
- **冗餘檔案全面肅清 (Redundancy Elimination)**：
  - 根目錄移除重複之 `期中報告_Antigravity全自動工作流程指南.md`，回歸收納於 `04_期中專題_DryBean/`。
  - 消除專案內部重複之 `MIDTERM_REPORT.md` 與 `midterm_slides.html`，統一於 `04_期中專題_DryBean/` 單一權威版本管理。
- **檔案命名語意化與週次時間軸排序 (Semantic & Chronological Renaming)**：
  - `01_課程大綱與導讀作業/`：將代號檔名 `S__4849709.jpg` 重命名為具備明確工程語意之 `期中專題SOP流程圖_S__4849709.jpg`。
  - `02_課堂授課投影片/`：全面為 4 份教學簡報加上週次前綴（`第01週_簡介`、`第01週_課程導讀`、`第03週_監督式學習`、`第05週_非監督式學習`），與 115-1 授課進度排程完全吻合。
- **簡報系統四大實用體驗升級 (`midterm_slides.html`)**：
  - **直接相對路徑**：全面將圖表路徑簡化為原生 `output/figures/*.png`，並保留智慧容錯機制。
  - **快速跳轉選單**：頂端導覽列實裝動態選單，演講時可於 18 頁投影片間一秒瞬移。
  - **列印匯出 PDF 支援**：導入 `@media print` 規範，瀏覽器 `Ctrl+P` 可直接匯出為 18 頁排版完美的高畫質 PDF。
  - **一鍵複製 PK 話術**：PK 攻防抽屜新增「📋 複製話術」按鈕，演練與實戰複製便捷。

---

## [v1.5.0] - 2026-10-13
### 🎯 指令三全面落地：20 分鐘互動式期中簡報與正式專題研究報告產出 (Deliverables & Presentation)
- **20 分鐘期中簡報系統 (`slides/midterm_slides.html`)**：
  - 打造現代深色科技風 (Dark Cyberpunk / Glassmorphism) 互動式投影片系統。
  - 完整涵蓋 **18 頁投影片**，嚴格對照工作流程指南之演講結構與配時規劃。
  - **核心互動功能**：
    - **20 分鐘總演講計時器**：內建自動倒數、狀態燈號（剩餘 5 分鐘警示黃燈、剩餘 2 分鐘急迫紅燈）、暫停/重置功能。
    - **講者講稿抽屜 (Speaker Notes Drawer)**：每頁皆收錄 150~250 字之專業逐字稿、口條要點與時間指引，可隨時按快捷鍵 `N` 展開。
    - **PK 攻防戰略抽屜 (PK Defense Drawer)**：內建 4 大進攻提問與 4 大防守話術，可隨時按快捷鍵 `P` 展開對戰手冊。
    - **高解析度圖表燈箱 (Image Lightbox Modal)**：點擊投影片中任一張圖表即可全螢幕無損放大檢視。
    - **完整鍵盤控制**：支援左右方向鍵換頁、`Space` 翻頁、`F` 全螢幕、`T` 計時開關、`Home`/`End` 首末頁跳轉。
- **正式期中專題研究報告 (`MIDTERM_REPORT.md`)**：
  - 撰寫六大章節長篇學術與工程綜合報告，完全遵循 $\text{Data} \to \text{Model} \to \text{Evaluation} \to \text{Explanation}$ 四部曲。
  - 涵蓋完整 LaTeX 數學公式推導（Gini Impurity, Euclidean Distance, Z-score Normalization, ARI, Purity, PCA Loading）。
  - 收錄全量實驗對比數據表：決策樹 12 個深度調參數據、隨機森林 16 個特徵重要度、7x7 混淆矩陣、高斯雜訊 0%~30% 壓力測試、K-Means 標準化前後量化對比。
  - 詳載近緣品種（SIRA vs DERMASON）物理幾何重疊之深層機理解析與多視角 3D 感測升級建議。
  - 收錄對戰第 13 組 (PK 組) 攻防手冊與程式重現指引。

---

## [v1.4.0] - 2026-10-13
### 🧠 指令二全面落地：雙軌機器學習模型訓練、特徵解釋與跨軌評估完成 (Dual-Track Modeling & Evaluation)
- **監督式學習管線 (`src/02_supervised_models.py`)**：
  - **決策樹深度超參數探索 (`max_depth`)**：
    - 遍歷深度 `[1, 2, 3, 4, 6, 8, 10, 12, 15, 20, 25, None]`。
    - 最佳深度為 `max_depth=15`，測試集準確率達 **90.29%**。
    - 完整驗證過擬合現象：當不限制深度 (`None`) 時，訓練集準確率達 100.00%，但測試集準確率反降至 89.55%，科學印證課堂 09/29 講義之「決策樹過擬合防範機制」。
    - 產出 `output/figures/03_dt_depth_vs_accuracy.png`（欠擬合、泛化良好、過擬合三階段對比曲線）。
    - 產出 `output/figures/04_decision_tree_structure.png`（深度 2 之高解釋性白箱規則樹狀圖）。
  - **隨機森林集成模型 (`n_estimators=100, max_depth=15`)**：
    - 測試集準確率大幅提升至 **92.06%**（訓練集 99.51%）。
    - 萃取 16 個特徵重要度權重，Top 5 關鍵特徵為：`ShapeFactor3` (10.49%)、`Perimeter` (10.07%)、`ShapeFactor1` (9.12%)、`Compactness` (9.07%)、`ConvexArea` (8.07%)。
    - 產出 `output/figures/05_rf_feature_importance.png`（特徵重要度橫向排序長條圖）。
  - **7x7 多分類混淆矩陣與物種辨識診斷**：
    - BOMBAY 品種達成 100% 精準度與 100% 召回率 (F1: 1.00)。
    - 深入診斷最大混淆源：SIRA (F1: 0.861) 與 DERMASON (F1: 0.918) 因生理幾何外觀極度相近，相互誤判（SIRA 誤判為 DERMASON 57 筆，DERMASON 誤判為 SIRA 41 筆，佔整體分類錯誤 80% 以上）。
    - 產出 `output/figures/06_confusion_matrix_comparison.png`（7x7 混淆矩陣熱力圖）。
  - **抗雜訊魯棒性加分實驗 (Noise Robustness Analysis)**：
    - 注入高斯雜訊 ($\sigma \in [0.0, 0.30]$)，隨機森林在 30% 強雜訊下仍維持 87.67% 準確率，而單一決策樹跌至 74.20%（相差 +13.47%），以量化實驗證實 Bagging 集成之抗擾動優勢。
- **非監督式學習管線 (`src/03_unsupervised_models.py`)**：
  - **K-Means ($K=7$) 標準化前後嚴謹對比**：
    - 未標準化：ARI 僅 0.3881，Purity 僅 58.76%（因 `Area` 數值尺度破萬，主導歐氏距離計算，壓制無量綱形狀因子）。
    - StandardScaler 標準化後：ARI 躍升至 **0.6669** (+27.88%)，Purity 躍升至 **79.76%** (+21.00%)！
    - 完美呼應教授 10/13 講義強調之「特徵尺度懸殊對距離度量之致命影響」。
    - 產出 `output/figures/07_kmeans_standardization_compare.png`（標準化前後對比雙散布圖）。
- **跨軌評估與主成分降維分析 (`src/04_cross_evaluation.py`)**：
  - PCA 2D 主成分投影：PC1 解釋變異量 55.55%，PC2 解釋變異量 26.36%，前兩主成分累積解釋變異量高達 **81.91%**。
  - 產出 `output/figures/08_cluster_vs_ground_truth.png`（真實標籤 vs K-Means 群聚並排對比圖）。
  - 匯出專案核心量化指標數據庫 `output/metrics_summary.json`、`supervised_metrics.json` 與 `unsupervised_metrics.json`。

---

## [v1.3.0] - 2026-10-13
### 🗂️ 全域檔案整理與架構優化 (Directory Optimization)
- **目錄重構**：將根目錄散落之所有課堂講義、作業記錄單、投影片與專案代碼進行分門別類，建立 4 大專屬資料夾：
  - `01_課程大綱與導讀作業/`：收納課程教學大綱 (`115-1 intro.pdf`)、每週導讀討論單 (`分組閱讀討論紀錄表_v1.docx`) 與期中作業 SOP 流程圖 (`S__4849709.jpg`)。
  - `02_課堂授課投影片/`：收納第 1 週至第 5 週之所有 PPTX 講義（AI 簡介、監督式學習決策樹/隨機森林、非監督式學習 K-Means）。
  - `03_課堂範例程式庫/`：收納教師提供之教學程式碼專案 `my-yzu-ai-course-main/`。
  - `04_期中專題_DryBean/`：收納期中選題簡報 (`人工智慧概論_期中報告選題.pdf`)、自動化流程指南，以及專案核心管線目錄 `midterm_drybean/`。
- **日誌系統上線**：
  - 建立 `CHANGELOG.md`（更新日誌）完整追蹤專案進度。
  - 建立 `ERROR_LOG.md`（報錯與修復日誌）記錄所有底層環境與程式排錯歷程。
  - 建立 `README.md`（檔案索引導覽地圖）提供清晰之檢索指引。

---

## [v1.2.0] - 2026-10-13
### 🚀 指令一落地：自動化資料前處理管線建置完成 (Data Pipeline Implemented)
- **Python 3.11 核心環境部署**：
  - 成功於 Windows 系統中部署獨立 Python 3.11.9 執行環境。
  - 建立獨立虛擬環境 `midterm_drybean/venv/`，安裝並驗證 `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `openpyxl`, `requests` 等核心套件。
- **資料自動下載與檢驗**：
  - 實作 `src/01_data_pipeline.py`，自動從 UCI 官網拉取 Dry Bean 資料集並解壓。
  - 完成資料品質檢核：總樣本 13,611 筆，缺失值 0 筆，自動識別並剔除 68 筆重複樣本，有效資料為 13,543 筆。
- **特徵工程與標準化切分**：
  - 嚴格採用 `stratify=y` 分層取樣切分 80% 訓練集 (10,834 筆) 與 20% 測試集 (2,709 筆)。
  - 產出未標準化與 `StandardScaler` 標準化版本特徵集。
- **高解析度圖表產出**：
  - 產出 `output/figures/01_class_distribution.png`（7 種豆種樣本數量與比例柱狀圖）。
  - 產出 `output/figures/02_correlation_heatmap.png`（16 個幾何特徵相關矩陣熱力圖）。
  - 修正 Matplotlib 字型設定，成功載入 `Microsoft JhengHei`，消除 CJK 豆腐塊亂碼。

---

## [v1.1.0] - 2026-10-13
### 📘 期中報告自動化工作流程藍圖規劃 (Workflow Blueprint)
- 撰寫 `期中報告_Antigravity全自動工作流程指南.md`。
- 確立「Data $\rightarrow$ Model $\rightarrow$ Evaluation $\rightarrow$ Explanation」四部曲架構。
- 規劃 20 分鐘期中簡報（18 頁 Slide）逐頁內容配時與講者講稿。
- 確立決策樹深度調參 (`max_depth`)、隨機森林集成、雜訊抗性加分實驗，以及 K-Means 標準化前後對比三大核心技術亮點。

---

## [v1.0.0] - 2026-10-13
### 🔍 專案初始化與教材探索 (Initial Ingestion)
- 探索工作區所有課程檔案，確認本組為**第 9 組**，對戰對手為**第 13 組**，鎖定研究主題為 **UCI Dry Bean Dataset**。
- 全面解析課堂投影片概念：
  - 監督式學習：決策樹門檻規則、過擬合現象、隨機森林抗雜訊能力。
  - 非監督式學習：K-Means 演算法邏輯、特徵尺度懸殊對歐氏距離之致命影響。

---

## 📅 專案里程碑完成狀態 (Project Status)
- [x] **v1.0.0**：專案初始化、課堂教材與投影片全面解析（鎖定第 9 組 vs 第 13 組，UCI Dry Bean）。
- [x] **v1.1.0**：期中全自動化流水線藍圖規劃 (`期中報告_Antigravity全自動工作流程指南.md`)。
- [x] **v1.2.0 (指令一)**：Python 3.11 環境部署、資料清洗、80/20 分層取樣與 EDA 圖表。
- [x] **v1.3.0**：全域目錄語意化重構，日誌系統 (`CHANGELOG.md`, `ERROR_LOG.md`, `README.md`) 上線。
- [x] **v1.4.0 (指令二)**：雙軌機器學習訓練（決策樹調參、隨機森林、抗雜訊測試、K-Means 標準化對比、PCA 降維、8 大發表級圖表）。
- [x] **v1.5.0 (指令三)**：20 分鐘互動式期中簡報系統 (`slides/midterm_slides.html`) 與正式期中專題研究報告 (`MIDTERM_REPORT.md`) 全面交付，PK 答辯攻防手冊備妥！
- **🚀 最終目標**：**2026/10/27（第八週）期中專題報告 20 分鐘現場簡報與對抗第 13 組 PK 賽取得全勝！**
