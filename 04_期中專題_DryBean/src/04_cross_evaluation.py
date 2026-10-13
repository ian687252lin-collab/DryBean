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

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
FIGURES_DIR = os.path.join(BASE_DIR, "output", "figures")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(FIGURES_DIR, exist_ok=True)

def generate_cross_evaluation_chart_and_summary():
    print("==================================================")
    print("雙軌交叉驗證 (Supervised vs Unsupervised Cross-Evaluation)")
    print("==================================================")
    
    csv_path = os.path.join(DATA_PROC_DIR, "dry_bean_cleaned.csv")
    df = pd.read_csv(csv_path)
    target_col = "Class"
    feature_cols = [c for c in df.columns if c != target_col]
    
    X = df[feature_cols]
    y = df[target_col]
    
    # 標準化與 PCA
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    var_exp = pca.explained_variance_ratio_
    
    # K-Means (K=7)
    kmeans = KMeans(n_clusters=7, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # 繪製圖表 8: 真實品種標籤 vs K-Means 自然分群邊界對照圖
    fig, axes = plt.subplots(1, 2, figsize=(18, 7.5))
    
    # 左圖：真實品種
    classes = sorted(y.unique())
    palette = sns.color_palette("tab10", len(classes))
    for i, cls in enumerate(classes):
        mask = (y == cls)
        axes[0].scatter(X_pca[mask, 0], X_pca[mask, 1], label=cls, color=palette[i], alpha=0.55, s=14)
    axes[0].set_title("地面真實標籤 (Ground Truth Varieties)\n監督式學習目標邊界", fontsize=14, fontweight='bold', pad=12)
    axes[0].set_xlabel(f"第一主成分 PC1 ({var_exp[0]*100:.1f}%)", fontsize=11)
    axes[0].set_ylabel(f"第二主成分 PC2 ({var_exp[1]*100:.1f}%)", fontsize=11)
    axes[0].legend(title="乾豆品種", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
    
    # 右圖：K-Means 分群
    cluster_palette = sns.color_palette("tab10", 7)
    for c in range(7):
        mask = (cluster_labels == c)
        axes[1].scatter(X_pca[mask, 0], X_pca[mask, 1], label=f"Cluster {c+1}", color=cluster_palette[c], alpha=0.55, s=14)
    axes[1].set_title("K-Means 自然聚類分群 (Unsupervised Clusters, K=7)\n非監督式學習幾何邊界", fontsize=14, fontweight='bold', pad=12)
    axes[1].set_xlabel(f"第一主成分 PC1 ({var_exp[0]*100:.1f}%)", fontsize=11)
    axes[1].set_ylabel(f"第二主成分 PC2 ({var_exp[1]*100:.1f}%)", fontsize=11)
    axes[1].legend(title="自然聚類群", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
    
    plt.suptitle("雙軌方法交叉比對：真實乾豆生物標籤 vs K-Means 自然形態聚類邊界", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    fig8_path = os.path.join(FIGURES_DIR, "08_cluster_vs_ground_truth.png")
    plt.savefig(fig8_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"已儲存圖表 8: {fig8_path}")
    
    # 匯總所有量化指標
    sup_metrics_path = os.path.join(OUTPUT_DIR, "supervised_metrics.json")
    unsup_metrics_path = os.path.join(OUTPUT_DIR, "unsupervised_metrics.json")
    
    sup_data = {}
    unsup_data = {}
    if os.path.exists(sup_metrics_path):
        with open(sup_metrics_path, "r", encoding="utf-8") as f:
            sup_data = json.load(f)
    if os.path.exists(unsup_metrics_path):
        with open(unsup_metrics_path, "r", encoding="utf-8") as f:
            unsup_data = json.load(f)
            
    summary = {
        "project_info": {
            "dataset_name": "UCI Dry Bean Dataset",
            "total_cleaned_samples": len(df),
            "features_count": len(feature_cols),
            "classes_count": len(classes),
            "classes_list": classes
        },
        "supervised_learning": {
            "best_decision_tree_depth": sup_data.get("best_dt_depth", 8),
            "decision_tree_test_accuracy": sup_data.get("best_dt_test_accuracy", 0.0),
            "random_forest_train_accuracy": sup_data.get("rf_train_accuracy", 0.0),
            "random_forest_test_accuracy": sup_data.get("rf_test_accuracy", 0.0),
            "top_5_feature_importances": sup_data.get("feature_importances_top5", []),
            "noise_robustness": sup_data.get("noise_robustness", {}),
            "per_class_f1_score": {
                cls: sup_data.get("class_report", {}).get(cls, {}).get("f1-score", 0.0)
                for cls in classes
            }
        },
        "unsupervised_learning": {
            "kmeans_raw_ari": unsup_data.get("ari_raw", 0.0),
            "kmeans_raw_purity": unsup_data.get("purity_raw", 0.0),
            "kmeans_scaled_ari": unsup_data.get("ari_scaled", 0.0),
            "kmeans_scaled_purity": unsup_data.get("purity_scaled", 0.0),
            "pca_pc1_explained_var": var_exp[0],
            "pca_pc2_explained_var": var_exp[1]
        }
    }
    
    master_json_path = os.path.join(OUTPUT_DIR, "metrics_summary.json")
    with open(master_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"已儲存期中專案量化總指標: {master_json_path}")
    print("==================================================")
    print("雙軌交叉驗證完成！全部 8 張高解析度圖表均已齊備！")
    print("==================================================")

if __name__ == "__main__":
    generate_cross_evaluation_chart_and_summary()
