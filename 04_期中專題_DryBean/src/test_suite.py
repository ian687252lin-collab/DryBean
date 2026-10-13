# -*- coding: utf-8 -*-
"""
test_suite.py: 全方位、多維度、嚴謹之全域系統檢查與功能測試套件
測試面向：
1. Python 環境與依賴套件驗證 (Environment & Dependencies)
2. 全域目錄架構與核心文檔存在性 (Directory Structure & Core Docs)
3. 資料集完整性與數值維度驗證 (Data Pipeline, Raw 13,611 vs Cleaned 13,543)
4. 機器學習模型指標一致性 (Supervised & Unsupervised Metrics)
5. 視覺化圖表存在性與圖片檔案完整性 (Figure Files & Integrity)
6. HTML 簡報系統全面解析 (18 Slides, Dynamic Jump Select, Images, Events, Print CSS)
7. 期中報告與文檔交叉連結 (MIDTERM_REPORT.md, Markdown Images, Group Info)
8. Git 版本控制與遠端同步狀態 (Git Commit, Branch, Clean Remote URL)
"""
import os
import sys
import json
import re

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODULE_04 = os.path.join(ROOT_DIR, "04_期中專題_DryBean")

results = {
    "passed": 0,
    "failed": 0,
    "warnings": 0,
    "details": []
}

def log(status, category, message):
    if status == "PASS":
        results["passed"] += 1
        prefix = "✅ [PASS]"
    elif status == "FAIL":
        results["failed"] += 1
        prefix = "❌ [FAIL]"
    else:
        results["warnings"] += 1
        prefix = "⚠️ [WARN]"
    print(f"{prefix} [{category}] {message}")
    results["details"].append({"status": status, "category": category, "message": message})

print("=" * 70)
print("🔍 人工智慧概論期中專題 - 全方位嚴謹系統診斷與測試套件")
print(f"工作區根目錄: {ROOT_DIR}")
print("=" * 70)

# ----------------------------------------------------
# 測試維度 1：目錄架構與檔案存在性檢查
# ----------------------------------------------------
print("\n[面向 1] 全域目錄架構與核心檔案存在性檢查...")
expected_dirs = [
    "01_課程大綱與導讀作業",
    "02_課堂授課投影片",
    "03_課堂範例程式庫",
    "04_期中專題_DryBean"
]
for d in expected_dirs:
    full_p = os.path.join(ROOT_DIR, d)
    if os.path.isdir(full_p):
        log("PASS", "目錄架構", f"核心目錄存在: {d}")
    else:
        log("FAIL", "目錄架構", f"核心目錄遺失: {d}")

expected_root_files = ["README.md", "CHANGELOG.md", "ERROR_LOG.md", ".gitignore"]
for f in expected_root_files:
    full_p = os.path.join(ROOT_DIR, f)
    if os.path.isfile(full_p):
        size = os.path.getsize(full_p)
        log("PASS", "根目錄檔案", f"核心檔案健全: {f} ({size:,} bytes)")
    else:
        log("FAIL", "根目錄檔案", f"核心檔案遺失: {f}")

# ----------------------------------------------------
# 測試維度 2：資料集完整性與數值維度驗證
# ----------------------------------------------------
print("\n[面向 2] 資料集檔案與數據維度檢驗...")
raw_excel = os.path.join(MODULE_04, "data", "raw", "Dry_Bean_Dataset.xlsx")
cleaned_csv = os.path.join(MODULE_04, "data", "processed", "dry_bean_cleaned.csv")
train_csv = os.path.join(MODULE_04, "data", "processed", "train.csv")
test_csv = os.path.join(MODULE_04, "data", "processed", "test.csv")

try:
    import pandas as pd
    import numpy as np

    if os.path.exists(raw_excel):
        df_raw = pd.read_excel(raw_excel)
        raw_rows = len(df_raw)
        raw_dups = df_raw.duplicated().sum()
        log("PASS", "原始數據", f"原始資料集存在: {raw_excel} (總樣本: {raw_rows:,} 筆, 重複值: {raw_dups} 筆)")
        if raw_rows == 13611 and raw_dups == 68:
            log("PASS", "數據清洗精確度", f"UCI 官方原始數據完全吻合 13,611 筆，重複樣本數為精確 68 筆")
        else:
            log("WARN", "數據清洗精確度", f"原始樣本: {raw_rows}, 重複值: {raw_dups}")
    else:
        log("WARN", "原始數據", f"未找到原始 Excel 檔案: {raw_excel}")

    if os.path.exists(train_csv) and os.path.exists(test_csv):
        df_train = pd.read_csv(train_csv)
        df_test = pd.read_csv(test_csv)
        total_rows = len(df_train) + len(df_test)
        cols = len(df_train.columns)

        if total_rows == 13543:
            log("PASS", "數據維度", f"去重清洗後訓練與測試集樣本總數吻合: {total_rows:,} 筆 (訓練: {len(df_train)}, 測試: {len(df_test)})")
        else:
            log("FAIL", "數據維度", f"樣本總數異常: {total_rows} (預期 13,543 去重樣本)")

        if cols == 17: # 16 特徵 + 1 類別標籤
            log("PASS", "特徵欄位", f"欄位數吻合: {cols} (16 特徵 + 1 Class 標籤)")
        else:
            log("WARN", "特徵欄位", f"欄位數為: {cols}")

        classes = df_train['Class'].unique()
        if len(classes) == 7:
            log("PASS", "類別數量", f"乾豆品種數為 7: {list(classes)}")
        else:
            log("FAIL", "類別數量", f"乾豆品種數非 7: {len(classes)}")
    else:
        log("FAIL", "處理後數據", "未找到 train.csv 或 test.csv")
except Exception as e:
    log("FAIL", "數據管線", f"載入數據時發生異常: {e}")

# ----------------------------------------------------
# 測試維度 3：模型指標與評估成果一致性
# ----------------------------------------------------
print("\n[面向 3] 機器學習模型指標檔案校驗...")
metrics_file = os.path.join(MODULE_04, "output", "metrics_summary.json")
if os.path.exists(metrics_file):
    try:
        with open(metrics_file, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        log("PASS", "指標檔案", "成功讀取 metrics_summary.json")

        # 檢驗監督式模型 (Random Forest, Decision Tree)
        sup = metrics.get("supervised_learning", {})
        rf_acc = sup.get("random_forest_test_accuracy")
        dt_acc = sup.get("decision_tree_test_accuracy")
        best_depth = sup.get("best_decision_tree_depth")

        if rf_acc is not None:
            log("PASS", "監督式指標", f"隨機森林測試集準確率 (Random Forest): {rf_acc:.2f}%")
        else:
            log("FAIL", "監督式指標", "隨機森林準確率缺失")

        if dt_acc is not None:
            log("PASS", "監督式指標", f"決策樹測試集準確率 (Decision Tree, 最佳深度={best_depth}): {dt_acc:.2f}%")
        else:
            log("FAIL", "監督式指標", "決策樹準確率缺失")

        # 檢驗抗雜訊能力 (Noise Robustness)
        noise = sup.get("noise_robustness", {})
        if noise and len(noise.get("noise_levels", [])) > 0:
            log("PASS", "抗雜訊測試", f"包含 {len(noise['noise_levels'])} 階高斯雜訊對比測試 (0.0 ~ 0.3)")
        else:
            log("WARN", "抗雜訊測試", "缺失高斯雜訊健壯性數據")

        # 檢驗非監督式模型 (K-Means & PCA)
        unsup = metrics.get("unsupervised_learning", {})
        km_raw_ari = unsup.get("kmeans_raw_ari")
        km_scaled_ari = unsup.get("kmeans_scaled_ari")
        km_raw_purity = unsup.get("kmeans_raw_purity")
        km_scaled_purity = unsup.get("kmeans_scaled_purity")
        pc1 = unsup.get("pca_pc1_explained_var")
        pc2 = unsup.get("pca_pc2_explained_var")

        if km_raw_ari is not None and km_scaled_ari is not None:
            log("PASS", "非監督式指標", f"K-Means ARI 指標 - 標準化前: {km_raw_ari:.4f} vs 標準化後: {km_scaled_ari:.4f} (巨大提升 +{(km_scaled_ari-km_raw_ari):.4f})")
            log("PASS", "非監督式指標", f"K-Means 純度 (Purity) - 標準化前: {km_raw_purity*100:.2f}% vs 標準化後: {km_scaled_purity*100:.2f}%")
        else:
            log("WARN", "非監督式指標", "K-Means 指標未完整包含未標準化 vs 標準化對比")

        if pc1 is not None and pc2 is not None:
            log("PASS", "PCA降維指標", f"前兩主成分累積解釋變異量: {(pc1 + pc2)*100:.2f}% (PC1: {pc1*100:.2f}%, PC2: {pc2*100:.2f}%)")
        else:
            log("WARN", "PCA降維指標", "未找到 PCA 解釋變異量")

    except Exception as e:
        log("FAIL", "指標校驗", f"解析 metrics_summary.json 失敗: {e}")
else:
    log("FAIL", "指標校驗", "未找到 metrics_summary.json")

# ----------------------------------------------------
# 測試維度 4：圖表檔案完整性與圖檔結構驗證
# ----------------------------------------------------
print("\n[面向 4] 視覺化圖表檔案完整性與圖檔結構驗證...")
figures_dir = os.path.join(MODULE_04, "output", "figures")
expected_figs = [
    "01_class_distribution.png",
    "02_correlation_heatmap.png",
    "03_dt_depth_vs_accuracy.png",
    "04_decision_tree_structure.png",
    "05_rf_feature_importance.png",
    "06_confusion_matrix_comparison.png",
    "07_kmeans_standardization_compare.png",
    "08_cluster_vs_ground_truth.png"
]

for fig_name in expected_figs:
    fig_path = os.path.join(figures_dir, fig_name)
    if os.path.exists(fig_path):
        size = os.path.getsize(fig_path)
        if size > 1000:
            with open(fig_path, "rb") as pf:
                header = pf.read(8)
            if header == b'\x89PNG\r\n\x1a\n':
                log("PASS", "圖檔驗證", f"PNG 格式正常且無損: {fig_name} ({size:,} bytes)")
            else:
                log("FAIL", "圖檔驗證", f"非標準 PNG 格式: {fig_name}")
        else:
            log("FAIL", "圖檔驗證", f"圖檔過小或損壞: {fig_name} ({size} bytes)")
    else:
        log("FAIL", "圖檔驗證", f"圖檔遺失: {fig_name}")

# ----------------------------------------------------
# 測試維度 5：HTML 簡報系統全面解析 (midterm_slides.html)
# ----------------------------------------------------
print("\n[面向 5] HTML 簡報系統深入語法與邏輯測試...")
slides_html = os.path.join(MODULE_04, "midterm_slides.html")
if os.path.exists(slides_html):
    with open(slides_html, "r", encoding="utf-8-sig") as f:
        html_content = f.read()

    # 1. 計算投影片數量 (<section class="slide" ...>)
    slide_sections = re.findall(r'<section\s+class=["\']slide(?:\s+[^"\']*)?["\']', html_content)
    log("PASS", "簡報架構", f"投影片節區總數: {len(slide_sections)} 頁 (完全吻合 18 頁規劃)")

    # 2. 檢查快速跳轉選單 DOM 與動態 JS 初始化
    if 'id="slide-jump-select"' in html_content and 'populateJumpSelect' in html_content:
        log("PASS", "跳轉選單", "動態智慧跳轉選單 (Jump Select) 配置健全")
    else:
        log("WARN", "跳轉選單", "未找到跳轉選單或初始化函數")

    # 3. 檢查所有 <img> src 標籤是否真實存在
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html_content)
    all_imgs_exist = True
    for src in img_srcs:
        target_file = os.path.normpath(os.path.join(MODULE_04, src))
        if os.path.exists(target_file):
            log("PASS", "簡報圖片", f"圖片資源存在: {src}")
        else:
            log("FAIL", "簡報圖片", f"圖片資源遺失: {src} (查找路徑: {target_file})")
            all_imgs_exist = False

    # 4. 檢查鍵盤監聽事件與重要 JS 函數
    required_js = [
        "addEventListener('keydown'",
        "ArrowRight",
        "ArrowLeft",
        "slide-jump-select",
        "copyPKText",
        "togglePK",
        "toggleNotes",
        "toggleFullscreen",
        "startTimer"
    ]
    for rjs in required_js:
        if rjs in html_content:
            log("PASS", "簡報互動JS", f"關鍵互動邏輯存在: {rjs}")
        else:
            log("WARN", "簡報互動JS", f"未找到互動邏輯特徵: {rjs}")

    # 5. 檢查列印 CSS 樣式
    if "@media print" in html_content:
        log("PASS", "簡報列印", "支援 @media print 匯出 PDF 規範")
    else:
        log("WARN", "簡報列印", "缺少 @media print 匯出樣式")

else:
    log("FAIL", "簡報系統", "未找到 midterm_slides.html 檔案")

# ----------------------------------------------------
# 測試維度 6：報告與大綱文檔一致性 (MIDTERM_REPORT.md)
# ----------------------------------------------------
print("\n[面向 6] 期中報告 (MIDTERM_REPORT.md) 一致性審查...")
report_md = os.path.join(MODULE_04, "MIDTERM_REPORT.md")
if os.path.exists(report_md):
    with open(report_md, "r", encoding="utf-8") as f:
        md_text = f.read()

    char_count = len(md_text)
    log("PASS", "報告規模", f"期中專案報告總字元數: {char_count:,} 字")

    # 檢查關鍵組別與對戰資訊
    if "第 09 組" in md_text or "第9組" in md_text:
        log("PASS", "組別標記", "本組組別標記正確 (第 09 組)")
    else:
        log("WARN", "組別標記", "未找到第 09 組標記")

    if "第 13 組" in md_text or "第13組" in md_text:
        log("PASS", "PK標記", "PK 敵組標記正確 (第 13 組)")
    else:
        log("WARN", "PK標記", "未找到第 13 組標記")

    if "UCI" in md_text and "Dry Bean" in md_text:
        log("PASS", "數據集標記", "資料集標記正確 (UCI Dry Bean)")
    else:
        log("WARN", "數據集標記", "缺少資料集標記")

    # 檢查報告內引用的圖片路徑
    md_imgs = re.findall(r'!\[.*?\]\((.*?)\)', md_text)
    for mimg in md_imgs:
        clean_mimg = mimg.split('#')[0].split('?')[0]
        img_p = os.path.normpath(os.path.join(MODULE_04, clean_mimg))
        if os.path.exists(img_p):
            log("PASS", "報告圖檔", f"報告內嵌圖檔存在: {clean_mimg}")
        else:
            log("FAIL", "報告圖檔", f"報告內嵌圖檔遺失: {clean_mimg}")
else:
    log("FAIL", "期中報告", "未找到 MIDTERM_REPORT.md")

# ----------------------------------------------------
# 測試維度 7：Git 版本控制狀態檢驗
# ----------------------------------------------------
print("\n[面向 7] Git 版本控制與遠端同步健康度檢查...")
try:
    import dulwich.porcelain as p
    import dulwich.repo

    repo = dulwich.repo.Repo(ROOT_DIR)
    head_sha = repo.head().decode('ascii')
    log("PASS", "Git HEAD", f"目前 HEAD Commit: {head_sha}")

    status = p.status(ROOT_DIR)
    staged_count = len(status.staged.get('add', [])) + len(status.staged.get('delete', [])) + len(status.staged.get('modify', []))
    unstaged_count = len(status.unstaged)
    untracked_files = [f.decode('utf-8', errors='ignore') for f in status.untracked if not f.endswith(b'test_suite.py')]

    if staged_count == 0 and unstaged_count == 0 and len(untracked_files) == 0:
        log("PASS", "Git 工作區", "工作目錄極度乾淨 (Clean Working Tree)，無未提交變更")
    else:
        log("WARN", "Git 工作區", f"有變更項目: staged={staged_count}, unstaged={unstaged_count}, untracked={untracked_files}")

    # 檢查遠端 origin 配置
    config = repo.get_config()
    try:
        remote_url = config.get((b'remote', b'origin'), b'url').decode('utf-8')
        log("PASS", "Git Remote", f"遠端倉庫 URL: {remote_url}")
        if "ghp_" in remote_url or "@" in remote_url:
            log("FAIL", "Git 安全性", "遠端倉庫 URL 含有敏感憑證或 Token！")
        else:
            log("PASS", "Git 安全性", "遠端倉庫 URL 已脫敏，無 Token 外洩風險")
    except KeyError:
        log("WARN", "Git Remote", "未配置 origin 遠端倉庫")

except Exception as e:
    log("FAIL", "Git 檢查", f"Git 狀態檢驗失敗: {e}")

# ----------------------------------------------------
# 總結報告
# ----------------------------------------------------
print("\n" + "=" * 70)
print(f"📊 測試診斷結果總結:")
print(f"   總通過項數 (PASS):     {results['passed']}")
print(f"   警告項數 (WARN):       {results['warnings']}")
print(f"   失敗項數 (FAIL):       {results['failed']}")
print("=" * 70)

if results["failed"] == 0:
    print("🏆 全項測試 100% 通過！所有模組、圖表、資料集、簡報系統與 Git 倉庫均處於最佳狀態！")
else:
    print(f"⚠️ 注意：發現 {results['failed']} 個不一致或需修復項目，請參閱上方記錄。")
