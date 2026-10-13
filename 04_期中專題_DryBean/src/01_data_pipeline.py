import os
import sys
import zipfile
import urllib.request

# 確保 Windows 終端能正常輸出 UTF-8
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 設定微軟正黑體字型，確保中文圖表完美顯示
font_path = "C:/Windows/Fonts/msjh.ttc"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
FIGURES_DIR = os.path.join(BASE_DIR, "output", "figures")

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROC_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

UCI_ZIP_URL = "https://archive.ics.uci.edu/static/public/602/dry+bean+dataset.zip"
ZIP_PATH = os.path.join(DATA_RAW_DIR, "dry_bean_dataset.zip")
EXCEL_PATH = os.path.join(DATA_RAW_DIR, "Dry_Bean_Dataset.xlsx")

def download_and_extract():
    print("==================================================")
    print("Step 1: 下載並檢查 UCI Dry Bean 資料集...")
    print("==================================================")
    
    if not os.path.exists(EXCEL_PATH):
        if not os.path.exists(ZIP_PATH):
            print(f"正在從 UCI 下載: {UCI_ZIP_URL} ...")
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(UCI_ZIP_URL, headers=headers)
            with urllib.request.urlopen(req) as response, open(ZIP_PATH, 'wb') as out_file:
                out_file.write(response.read())
            print(f"下載完成: {ZIP_PATH}")
        
        print("解壓縮資料集...")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            for member in zip_ref.namelist():
                if member.endswith(".xlsx") or member.endswith(".csv"):
                    filename = os.path.basename(member)
                    if filename:
                        target = os.path.join(DATA_RAW_DIR, filename)
                        with zip_ref.open(member) as source, open(target, "wb") as dest:
                            dest.write(source.read())
                        print(f"解壓檔案: {target}")
    else:
        print(f"已存在原始資料檔: {EXCEL_PATH}")

def load_dataset():
    if os.path.exists(EXCEL_PATH):
        print(f"載入 Excel 格式資料: {EXCEL_PATH}")
        df = pd.read_excel(EXCEL_PATH)
    else:
        csv_candidates = [os.path.join(DATA_RAW_DIR, f) for f in os.listdir(DATA_RAW_DIR) if f.endswith(".csv")]
        if csv_candidates:
            print(f"載入 CSV 格式資料: {csv_candidates[0]}")
            df = pd.read_csv(csv_candidates[0])
        else:
            raise FileNotFoundError("未找到 Dry Bean 資料檔案！")
    return df

def clean_and_preprocess(df):
    print("==================================================")
    print("Step 2: 資料完整性檢查與清洗...")
    print("==================================================")
    print(f"原始資料維度: {df.shape[0]} 筆樣本, {df.shape[1]} 個欄位")
    
    # 檢查缺失值
    null_counts = df.isnull().sum().sum()
    print(f"缺失值數量: {null_counts}")
    
    # 檢查重複值
    dup_counts = df.duplicated().sum()
    print(f"重複值數量: {dup_counts}")
    if dup_counts > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"移除重複值後資料維度: {df.shape[0]} 筆樣本")
        
    target_col = "Class"
    feature_cols = [c for c in df.columns if c != target_col]
    print(f"特徵欄位數量: {len(feature_cols)}")
    print(f"目標類別 ('{target_col}') 分佈：")
    class_counts = df[target_col].value_counts()
    for cls_name, cnt in class_counts.items():
        pct = (cnt / len(df)) * 100
        print(f"  - {cls_name:10s}: {cnt:5d} 筆 ({pct:5.2f}%)")
        
    # 儲存清洗後完整資料
    cleaned_csv = os.path.join(DATA_PROC_DIR, "dry_bean_cleaned.csv")
    df.to_csv(cleaned_csv, index=False)
    print(f"已儲存清洗資料: {cleaned_csv}")
    
    return df, feature_cols, target_col

def generate_eda_figures(df, feature_cols, target_col):
    print("==================================================")
    print("Step 3: 繪製探索性分析 (EDA) 高解析度圖表...")
    print("==================================================")
    
    # 圖 1: 品種分佈圖 (Class Distribution)
    plt.figure(figsize=(10, 6))
    counts = df[target_col].value_counts()
    colors = sns.color_palette("viridis", len(counts))
    bars = plt.bar(counts.index, counts.values, color=colors, edgecolor='black', alpha=0.85)
    
    for bar in bars:
        yval = bar.get_height()
        pct = (yval / len(df)) * 100
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 50, f"{yval}\n({pct:.1f}%)", 
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.title("UCI Dry Bean 資料集 - 7 種乾豆品種樣本數量分佈", fontsize=15, pad=15, fontweight='bold')
    plt.xlabel("乾豆品種 (Bean Class)", fontsize=12, labelpad=10)
    plt.ylabel("樣本筆數 (Count)", fontsize=12, labelpad=10)
    plt.ylim(0, max(counts.values) * 1.15)
    plt.tight_layout()
    fig1_path = os.path.join(FIGURES_DIR, "01_class_distribution.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"已儲存圖表 1: {fig1_path}")
    
    # 圖 2: 16 個特徵相關係數熱力圖 (Correlation Heatmap)
    plt.figure(figsize=(14, 11))
    corr = df[feature_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    
    sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, annot=True, 
                fmt=".2f", square=True, linewidths=.5, cbar_kws={"shrink": .8})
    plt.title("UCI Dry Bean - 16 個形態特徵相關係數熱力圖 (Pearson Correlation)", fontsize=16, pad=20, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    fig2_path = os.path.join(FIGURES_DIR, "02_correlation_heatmap.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"已儲存圖表 2: {fig2_path}")

def split_and_scale_data(df, feature_cols, target_col):
    print("==================================================")
    print("Step 4: 分層切分 (Stratified Split) 與標準化...")
    print("==================================================")
    
    X = df[feature_cols]
    y = df[target_col]
    
    # 80% 訓練集, 20% 測試集, 維持品種比例
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    print(f"訓練集筆數: {len(X_train)} (80%)")
    print(f"測試集筆數: {len(X_test)} (20%)")
    
    # 儲存原始尺度切分資料
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    train_df.to_csv(os.path.join(DATA_PROC_DIR, "train.csv"), index=False)
    test_df.to_csv(os.path.join(DATA_PROC_DIR, "test.csv"), index=False)
    
    # 標準化 (StandardScaler)
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_cols)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=feature_cols)
    
    train_scaled_df = pd.concat([X_train_scaled, y_train.reset_index(drop=True)], axis=1)
    test_scaled_df = pd.concat([X_test_scaled, y_test.reset_index(drop=True)], axis=1)
    
    train_scaled_df.to_csv(os.path.join(DATA_PROC_DIR, "train_scaled.csv"), index=False)
    test_scaled_df.to_csv(os.path.join(DATA_PROC_DIR, "test_scaled.csv"), index=False)
    print(f"已儲存標準化特徵集至: {DATA_PROC_DIR}")
    print("==================================================")
    print("資料前處理管線 (Pipeline 1) 全部執行成功！")
    print("==================================================")

if __name__ == "__main__":
    download_and_extract()
    raw_df = load_dataset()
    clean_df, feats, target = clean_and_preprocess(raw_df)
    generate_eda_figures(clean_df, feats, target)
    split_and_scale_data(clean_df, feats, target)
