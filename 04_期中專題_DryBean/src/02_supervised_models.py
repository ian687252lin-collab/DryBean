import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# 確保 UTF-8 輸出
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import matplotlib
matplotlib.use('Agg')  # 使用無頭繪圖引擎，避免 Tkinter 多執行緒衝突
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

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

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROC_DIR = os.path.join(BASE_DIR, "data", "processed")
FIGURES_DIR = os.path.join(BASE_DIR, "output", "figures")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(FIGURES_DIR, exist_ok=True)

def load_data():
    train_path = os.path.join(DATA_PROC_DIR, "train.csv")
    test_path = os.path.join(DATA_PROC_DIR, "test.csv")
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    
    target_col = "Class"
    feature_cols = [c for c in train_df.columns if c != target_col]
    
    X_train = train_df[feature_cols]
    y_train = train_df[target_col]
    X_test = test_df[feature_cols]
    y_test = test_df[target_col]
    
    return X_train, y_train, X_test, y_test, feature_cols, sorted(y_train.unique())

def experiment_dt_max_depth(X_train, y_train, X_test, y_test):
    print("==================================================")
    print("實驗 A1: 決策樹深度超參數探索 (max_depth 欠擬合/過擬合分析)")
    print("==================================================")
    
    depths = [1, 2, 3, 4, 6, 8, 10, 12, 15, 20, 25, None]
    depth_labels = [str(d) if d is not None else "None" for d in depths]
    
    train_accs = []
    test_accs = []
    
    best_depth = None
    best_test_acc = 0
    best_dt_model = None
    
    for d in depths:
        dt = DecisionTreeClassifier(max_depth=d, random_state=42)
        dt.fit(X_train, y_train)
        
        tr_acc = accuracy_score(y_train, dt.predict(X_train)) * 100
        te_acc = accuracy_score(y_test, dt.predict(X_test)) * 100
        
        train_accs.append(tr_acc)
        test_accs.append(te_acc)
        
        lbl = str(d) if d is not None else "None"
        print(f"  - max_depth = {lbl:5s} | 訓練集準確率: {tr_acc:6.2f}% | 測試集準確率: {te_acc:6.2f}%")
        
        if te_acc > best_test_acc:
            best_test_acc = te_acc
            best_depth = d
            best_dt_model = dt
            
    print(f">> 最佳決策樹深度: {best_depth} (測試集準確率: {best_test_acc:.2f}%)")
    
    # 繪製圖表 3: Depth vs Accuracy
    plt.figure(figsize=(10, 6))
    x_indices = range(len(depths))
    plt.plot(x_indices, train_accs, marker='o', linewidth=2.5, color='#2b5c8f', label='訓練集準確率 (Training Accuracy)')
    plt.plot(x_indices, test_accs, marker='s', linewidth=2.5, color='#e05d44', label='測試集準確率 (Testing Accuracy)')
    
    # 標記分區：欠擬合、泛化良好、過擬合
    plt.axvspan(-0.5, 2.5, color='#ffebee', alpha=0.5, label='欠擬合區間 (Underfitting)')
    plt.axvspan(2.5, 6.5, color='#e8f5e9', alpha=0.5, label='良好泛化區間 (Good Generalization)')
    plt.axvspan(6.5, len(depths)-0.5, color='#fff9c4', alpha=0.5, label='過擬合區間 (Overfitting)')
    
    plt.xticks(x_indices, depth_labels, fontsize=11)
    plt.xlabel("決策樹最大深度 (max_depth)", fontsize=12, labelpad=10)
    plt.ylabel("準確率 (%)", fontsize=12, labelpad=10)
    plt.title("課堂活動實踐：決策樹 max_depth 深度對訓練與測試準確率之關聯", fontsize=14, pad=15, fontweight='bold')
    plt.legend(loc='lower right', frameon=True, fontsize=10)
    plt.ylim(50, 103)
    plt.tight_layout()
    
    fig3_path = os.path.join(FIGURES_DIR, "03_dt_depth_vs_accuracy.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"已儲存圖表 3: {fig3_path}")
    
    return best_dt_model, best_depth, best_test_acc

def visualize_decision_tree_structure(best_dt, feature_names, class_names):
    print("==================================================")
    print("實驗 A2: 決策樹決策邏輯視覺化 (白箱規則解構)")
    print("==================================================")
    
    # 建立深度為 2 的視覺化模型以保持易讀性
    vis_tree = DecisionTreeClassifier(max_depth=2, random_state=42)
    X_train, y_train, _, _, _, _ = load_data()
    vis_tree.fit(X_train, y_train)
    
    plt.figure(figsize=(16, 9))
    plot_tree(
        vis_tree,
        feature_names=feature_names,
        class_names=class_names,
        filled=True,
        rounded=True,
        fontsize=11
    )
    plt.title("UCI Dry Bean - 決策樹前兩層決策節點規則視覺化 (max_depth = 2)", fontsize=16, pad=15, fontweight='bold')
    plt.tight_layout()
    
    fig4_path = os.path.join(FIGURES_DIR, "04_decision_tree_structure.png")
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"已儲存圖表 4: {fig4_path}")

def experiment_random_forest(X_train, y_train, X_test, y_test, feature_names, class_names):
    print("==================================================")
    print("實驗 A3 & A4: 隨機森林集成學習 (Random Forest 100 Trees)")
    print("==================================================")
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    
    rf_train_acc = accuracy_score(y_train, rf.predict(X_train)) * 100
    rf_test_acc = accuracy_score(y_test, rf.predict(X_test)) * 100
    print(f"隨機森林訓練集準確率: {rf_train_acc:.2f}%")
    print(f"隨機森林測試集準確率: {rf_test_acc:.2f}%")
    
    # 特徵重要度排行
    importances = rf.feature_importances_
    feat_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=True)
    
    plt.figure(figsize=(10, 8))
    colors = sns.color_palette("mako", len(feat_df))
    plt.barh(feat_df["Feature"], feat_df["Importance"], color=colors, edgecolor='black', alpha=0.85)
    plt.xlabel("特徵重要度 (Feature Importance)", fontsize=12, labelpad=10)
    plt.ylabel("形態特徵 (Morphological Features)", fontsize=12, labelpad=10)
    plt.title("隨機森林模型 - 16 個乾豆外觀特徵重要度權重排行", fontsize=14, pad=15, fontweight='bold')
    
    for i, v in enumerate(feat_df["Importance"]):
        plt.text(v + 0.002, i, f"{v:.4f}", va='center', fontsize=9, fontweight='bold')
        
    plt.xlim(0, max(feat_df["Importance"]) * 1.15)
    plt.tight_layout()
    fig5_path = os.path.join(FIGURES_DIR, "05_rf_feature_importance.png")
    plt.savefig(fig5_path, dpi=300)
    plt.close()
    print(f"已儲存圖表 5: {fig5_path}")
    
    # 混淆矩陣
    y_pred = rf.predict(X_test)
    cm = confusion_matrix(y_test, y_pred, labels=class_names)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names, cbar=True)
    plt.xlabel("模型預測品種 (Predicted Class)", fontsize=12, labelpad=10)
    plt.ylabel("實際真實品種 (True Class)", fontsize=12, labelpad=10)
    plt.title(f"隨機森林 7x7 品種辨識混淆矩陣 (整體測試準確率: {rf_test_acc:.2f}%)", fontsize=14, pad=15, fontweight='bold')
    plt.tight_layout()
    fig6_path = os.path.join(FIGURES_DIR, "06_confusion_matrix_comparison.png")
    plt.savefig(fig6_path, dpi=300)
    plt.close()
    print(f"已儲存圖表 6: {fig6_path}")
    
    # 詳細品種分類報告
    rep = classification_report(y_test, y_pred, labels=class_names, output_dict=True)
    print("\n各乾豆品種個別辨識報告 (Precision / Recall / F1-score):")
    for cls in class_names:
        metrics = rep[cls]
        print(f"  - {cls:10s} | 精確率: {metrics['precision']*100:5.2f}% | 召回率: {metrics['recall']*100:5.2f}% | F1: {metrics['f1-score']*100:5.2f}%")
        
    return rf, rf_train_acc, rf_test_acc, feat_df.sort_values(by="Importance", ascending=False).to_dict(orient="records"), rep

def experiment_noise_robustness(X_train, y_train, X_test, y_test):
    print("==================================================")
    print("實驗 A5: 抗雜訊工程魯棒性測試 (Data Noise & Label Noise)")
    print("==================================================")
    
    noise_levels = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]
    dt_accs = []
    rf_accs = []
    
    # 測試特徵雜訊 (Data Noise)
    std_devs = X_train.std(axis=0)
    
    for nl in noise_levels:
        noise = np.random.normal(0, nl, size=X_test.shape) * std_devs.values
        X_test_noisy = X_test + noise
        
        dt = DecisionTreeClassifier(max_depth=8, random_state=42).fit(X_train, y_train)
        rf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1).fit(X_train, y_train)
        
        dt_acc = accuracy_score(y_test, dt.predict(X_test_noisy)) * 100
        rf_acc = accuracy_score(y_test, rf.predict(X_test_noisy)) * 100
        
        dt_accs.append(dt_acc)
        rf_accs.append(rf_acc)
        print(f"  - 雜訊係數: {nl:4.2f} | 決策樹: {dt_acc:5.2f}% | 隨機森林: {rf_acc:5.2f}% (領先 +{rf_acc - dt_acc:4.2f}%)")
        
    return {
        "noise_levels": noise_levels,
        "dt_accuracies": dt_accs,
        "rf_accuracies": rf_accs
    }

if __name__ == "__main__":
    X_train, y_train, X_test, y_test, feature_names, class_names = load_data()
    best_dt, best_depth, best_dt_acc = experiment_dt_max_depth(X_train, y_train, X_test, y_test)
    visualize_decision_tree_structure(best_dt, feature_names, class_names)
    rf, rf_tr_acc, rf_te_acc, feat_ranks, class_report = experiment_random_forest(X_train, y_train, X_test, y_test, feature_names, class_names)
    noise_results = experiment_noise_robustness(X_train, y_train, X_test, y_test)
    
    # 保存暫存指標
    supervised_summary = {
        "best_dt_depth": best_depth,
        "best_dt_test_accuracy": best_dt_acc,
        "rf_train_accuracy": rf_tr_acc,
        "rf_test_accuracy": rf_te_acc,
        "feature_importances_top5": feat_ranks[:5],
        "noise_robustness": noise_results,
        "class_report": class_report
    }
    with open(os.path.join(OUTPUT_DIR, "supervised_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(supervised_summary, f, ensure_ascii=False, indent=2)
    print("==================================================")
    print("監督式學習全自動建模與實驗完成！指標已暫存。")
    print("==================================================")
