import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 確保 UTF-8 輸出
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 設定字型
font_path = "C:/Windows/Fonts/msjh.ttc"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans']

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
FIGURES_DIR = os.path.join(BASE_DIR, "output", "figures")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(FIGURES_DIR, exist_ok=True)

def load_data():
    csv_path = os.path.join(DATA_PROC_DIR, "dry_bean_cleaned.csv")
    df = pd.read_csv(csv_path)
    target_col = "Class"
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols]
    y = df[target_col]
    return df, X, y, feature_cols

def calculate_purity(y_true, cluster_labels):
    contingency_matrix = pd.crosstab(y_true, cluster_labels)
    return np.sum(contingency_matrix.max(axis=0)) / len(y_true)

def experiment_kmeans_standardization(df, X, y, feature_cols):
    print("==================================================")
    print("實驗 B1: K-Means (K=7) 有無標準化致命對比實驗")
    print("==================================================")
    
    # Model A: 未標準化
    print("訓練 Model A (未標準化)...")
    kmeans_raw = KMeans(n_clusters=7, random_state=42, n_init=10)
    labels_raw = kmeans_raw.fit_predict(X)
    
    ari_raw = adjusted_rand_score(y, labels_raw)
    nmi_raw = normalized_mutual_info_score(y, labels_raw)
    purity_raw = calculate_purity(y, labels_raw)
    
    print(f"Model A (未標準化) | ARI: {ari_raw:.4f} | NMI: {nmi_raw:.4f} | 純度 (Purity): {purity_raw*100:.2f}%")
    
    # Model B: 有標準化 (StandardScaler)
    print("訓練 Model B (StandardScaler 標準化)...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans_scaled = KMeans(n_clusters=7, random_state=42, n_init=10)
    labels_scaled = kmeans_scaled.fit_predict(X_scaled)
    
    ari_scaled = adjusted_rand_score(y, labels_scaled)
    nmi_scaled = normalized_mutual_info_score(y, labels_scaled)
    purity_scaled = calculate_purity(y, labels_scaled)
    
    print(f"Model B (有標準化) | ARI: {ari_scaled:.4f} | NMI: {nmi_scaled:.4f} | 純度 (Purity): {purity_scaled*100:.2f}%")
    print(f">> 標準化後 ARI 提升: +{(ari_scaled - ari_raw)*100:.2f}%，分群純度提升: +{(purity_scaled - purity_raw)*100:.2f}%")
    
    # PCA 2D 降維投影
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    var_exp = pca.explained_variance_ratio_
    print(f"PCA 主成分解釋變異量: PC1={var_exp[0]*100:.2f}%, PC2={var_exp[1]*100:.2f}% (累積: {sum(var_exp)*100:.2f}%)")
    
    # 繪製圖表 7: 標準化前後對比 (2 Subplots)
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    scatter1 = axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_raw, cmap='tab10', alpha=0.5, s=12)
    axes[0].set_title(f"Model A：未標準化 K-Means 分群\n(ARI = {ari_raw:.3f}, 純度 = {purity_raw*100:.1f}%)", fontsize=13, fontweight='bold', pad=10)
    axes[0].set_xlabel(f"第一主成分 PC1 ({var_exp[0]*100:.1f}%)", fontsize=11)
    axes[0].set_ylabel(f"第二主成分 PC2 ({var_exp[1]*100:.1f}%)", fontsize=11)
    axes[0].text(0.05, 0.92, "[!] 特徵數值尺度懸殊\n分群結果完全被 Area 支配", transform=axes[0].transAxes, 
                 fontsize=10, bbox=dict(boxstyle="round", facecolor='#ffcdd2', alpha=0.8))
    
    scatter2 = axes[1].scatter(X_pca[:, 0], X_pca[:, 1], c=labels_scaled, cmap='tab10', alpha=0.5, s=12)
    axes[1].set_title(f"Model B：標準化後 K-Means 分群\n(ARI = {ari_scaled:.3f}, 純度 = {purity_scaled*100:.1f}%)", fontsize=13, fontweight='bold', pad=10)
    axes[1].set_xlabel(f"第一主成分 PC1 ({var_exp[0]*100:.1f}%)", fontsize=11)
    axes[1].set_ylabel(f"第二主成分 PC2 ({var_exp[1]*100:.1f}%)", fontsize=11)
    axes[1].text(0.05, 0.92, "[OK] 特徵權重平衡\n形成清晰自然群聚簇", transform=axes[1].transAxes, 
                 fontsize=10, bbox=dict(boxstyle="round", facecolor='#c8e6c9', alpha=0.8))
    
    plt.suptitle("課堂核心驗證：特徵標準化對 K-Means 分群歐氏距離之關鍵影響 (K=7)", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    fig7_path = os.path.join(FIGURES_DIR, "07_kmeans_standardization_compare.png")
    plt.savefig(fig7_path, dpi=300)
    plt.close()
    print(f"已儲存圖表 7: {fig7_path}")
    
    df["Cluster_Scaled"] = labels_scaled
    df["PC1"] = X_pca[:, 0]
    df["PC2"] = X_pca[:, 1]
    
    return {
        "ari_raw": ari_raw,
        "nmi_raw": nmi_raw,
        "purity_raw": purity_raw,
        "ari_scaled": ari_scaled,
        "nmi_scaled": nmi_scaled,
        "purity_scaled": purity_scaled,
        "pca_variance_ratio": var_exp.tolist()
    }, df

if __name__ == "__main__":
    df, X, y, feature_cols = load_data()
    metrics, df_clustered = experiment_kmeans_standardization(df, X, y, feature_cols)
    
    # 儲存分群數據
    clustered_csv = os.path.join(DATA_PROC_DIR, "dry_bean_clustered.csv")
    df_clustered.to_csv(clustered_csv, index=False)
    
    with open(os.path.join(OUTPUT_DIR, "unsupervised_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print("==================================================")
    print("非監督式學習全自動建模與實驗完成！指標已暫存。")
    print("==================================================")
