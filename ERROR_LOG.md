# 專案報錯與問題修復日誌 (ERROR LOG)

本文件詳實記錄在全自動化管線建置、環境部署、套件安裝、數據前處理與繪圖過程中遭遇的所有錯誤訊息、根本原因分析 (Root Cause Analysis) 以及具體修復方案，以利團隊覆核與技術回溯。

---

## 報錯記錄目錄
1. [ERR-001：系統預設環境找不到 Python 指令](#err-001系統預設環境找不到-python-指令)
2. [ERR-002：Winget 安裝 Python 3.11 遭遇 Exit Code 50](#err-002winget-安裝-python-311-遭遇-exit-code-50)
3. [ERR-003：Windows 終端 cp950 編碼無法輸出 Unicode 打勾符號](#err-003windows-終端-cp950-編碼無法輸出-unicode-打勾符號)
4. [ERR-004：Matplotlib 繪製圖表出現 CJK 豆腐塊亂碼與字型警告](#err-004matplotlib-繪製圖表出現-cjk-豆腐塊亂碼與字型警告)
5. [ERR-005：目錄重構搬移對虛擬環境與腳本路徑之潛在衝擊](#err-005目錄重構搬移對虛擬環境與腳本路徑之潛在衝擊)
6. [ERR-006：Matplotlib 預設 Tkinter GUI 後端在 Windows 背景多執行緒中拋出 Tcl 異步釋放錯誤](#err-006matplotlib-預設-tkinter-gui-後端在-windows-背景多執行緒中拋出-tcl-異步釋放錯誤)
7. [ERR-007：嵌套巢狀子目錄導致相對路徑與圖表連結分化之架構缺陷](#err-007嵌套巢狀子目錄導致相對路徑與圖表連結分化之架構缺陷)

---

### ERR-001：系統預設環境找不到 Python 指令
- **發生階段**：Phase 1 環境檢測階段
- **錯誤現象**：執行 `python` 或 `py` 時，系統回傳：
  ```text
  Python was not found; run without arguments to install from the Microsoft Store, 
  or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
  ```
- **根本原因**：用戶之 Windows 主機目前尚未配置全域 Python 環境，僅有 Windows 預設之空捷徑引導。
- **解決方案**：
  - 規劃由 Antigravity 透過腳本自動化部署獨立之 Python 3.11 執行環境，並建立獨立於系統之專用虛擬環境 (`venv`)。

---

### ERR-002：Winget 安裝 Python 3.11 遭遇 Exit Code 50
- **發生階段**：Phase 1 自動化安裝 Python 階段
- **錯誤現象**：
  ```text
  Starting package install...
  Installer failed with exit code: 50
  Exit code: 0x32
  ```
- **根本原因**：
  - 解析 Windows 診斷安裝日誌發現，安裝包內部組件 `WixBundleLog_launcher_AllUsers` 預設嘗試為「所有使用者 (All Users)」安裝 `py.exe` 啟動器，需要 Administrator UAC 提權授權；在背景無聲安裝模式下無法彈窗提權，導致 MSI 安装器終止並回傳代碼 50 (`ERROR_NOT_SUPPORTED`)。
- **解決方案**：
  - 使用 PowerShell 直接自 Python 官方伺服器下載 `python-3.11.9-amd64.exe` 安裝程式。
  - 明確傳入免提權之使用者層級安裝參數：
    ```powershell
    Start-Process -FilePath $installer -ArgumentList "/quiet InstallAllUsers=0 Include_launcher=0 Include_test=0 SimpleInstall=1 PrependPath=1" -Wait
    ```
  - 安裝程序成功以 `ExitCode: 0` 完成安裝，Python 3.11.9 成功部署至 `%LOCALAPPDATA%\Programs\Python\Python311\`。

---

### ERR-003：Windows 終端 cp950 編碼無法輸出 Unicode 打勾符號
- **發生階段**：Phase 1 執行 `src/00_verify_env.py` 環境驗證時
- **錯誤訊息**：
  ```text
  Traceback (most recent call last):
    File "...\00_verify_env.py", line 26, in <module>
      print(f"  [\u2713] {pkg:15s}: {ver}")
  UnicodeEncodeError: 'cp950' codec can't encode character '\u2713' in position 3: illegal multibyte sequence
  ```
- **根本原因**：繁體中文 Windows 預設終端字碼頁為 `cp950`（Big5 擴充），無法編碼 Unicode 字符 `\u2713` (✓) 及 `\u2717` (✗)。
- **解決方案**：
  - 於 `00_verify_env.py` 中將展示字元改為純 ASCII 格式 `[OK]` 與 `[FAIL]`。
  - 於後續所有 Python 腳本開頭加入標準 UTF-8 輸出重配邏輯：
    ```python
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    ```
  - 重新執行後驗證腳本順利通過，輸出正常。

---

### ERR-004：Matplotlib 繪製圖表出現 CJK 豆腐塊亂碼與字型警告
- **發生階段**：Phase 2 執行 `src/01_data_pipeline.py` 產出 EDA 圖表時
- **錯誤訊息**：
  ```text
  UserWarning: Glyph 25976 (\N{CJK UNIFIED IDEOGRAPH-6578}) missing from font(s) Arial.
  ```
  產出之 `01_class_distribution.png` 標題與座標軸上的中文字元呈現空心方框（豆腐塊）。
- **根本原因**：Matplotlib 預設 sans-serif 字型清單優先搜尋 `Arial`，未成功索引系統中文字型檔。
- **解決方案**：
  - 透過 `matplotlib.font_manager.addfont()` 直接載入 Windows 系統字型 `C:/Windows/Fonts/msjh.ttc`（微軟正黑體），並設置全局字型參數：
    ```python
    import matplotlib.font_manager as fm
    font_path = "C:/Windows/Fonts/msjh.ttc"
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    ```
  - 重新繪圖後，所有中文標題、座標軸文字與百分比標籤皆以原生高解析度字體清晰呈現。

---

### ERR-005：目錄重構搬移對虛擬環境與腳本路徑之潛在衝擊
- **發生階段**：全域檔案整理與分類優化階段
- **潛在風險**：
  - 將專案由根目錄搬移至 `04_期中專題_DryBean/midterm_drybean/` 後，若腳本使用寫死之絕對路徑，可能導致 `FileNotFoundError`。
  - 虛擬環境 `venv` 的 `pyvenv.cfg` 中之 `command` 仍記錄原路徑。
- **防禦設計與驗證**：
  - 在 `src/01_data_pipeline.py` 中一律使用相對當前腳本動態錨定之根目錄：
    ```python
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ```
  - 在 Windows 中，`venv\Scripts\python.exe` 執行時主要依據自身目錄內的 `pyvenv.cfg` 中的 `home` 指向，實際測試搬移後直接調用 `.\04_期中專題_DryBean\midterm_drybean\venv\Scripts\python.exe`。
  - 執行驗證腳本與前處理腳本，回傳狀態碼皆為 `ExitCode: 0`，確認搬移後完全穩定運作。

---

### ERR-006：Matplotlib 預設 Tkinter GUI 後端在 Windows 背景多執行緒中拋出 Tcl 異步釋放錯誤
- **發生階段**：Phase 2 執行 `src/02_supervised_models.py` 繪製決策樹結構圖時
- **錯誤現象**：終端噴出錯誤並提示：
  ```text
  Tcl_AsyncDelete: async handler deleted by the wrong thread
  Fatal Python error: PyEval_SaveThread: NULL tstate
  ```
- **根本原因**：Windows 環境下 Matplotlib 預設使用互動式 GUI 後端（TkAgg）。當腳本在批次模式或無顯示終端環境下密集繪製並保存大圖 (`plt.savefig`) 時，Tkinter 於主線程退出時觸發了非線程安全的 C 語言層級異步清理崩潰。
- **解決方案**：
  - 在所有涉及繪圖的 Python 腳本最頂層（在 `import matplotlib.pyplot as plt` 之前），強制指定無頭後端 (Headless backend) `Agg`：
    ```python
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    ```
  - 重新執行腳本後，8 張超高解析度圖表皆無阻礙產出，進程平穩退出，回傳代碼為 0。

---

### ERR-007：嵌套巢狀子目錄導致相對路徑與圖表連結分化之架構缺陷
- **發生階段**：全域架構二次審查與目錄重構階段
- **問題現象**：`04_期中專題_DryBean/` 內部額外嵌套一層 `midterm_drybean/`，造成報告與簡報在兩層資料夾皆存在副本；且需要借助 Windows 目錄交聯 (Junction) 方能維持圖表相對路徑，增加了專案維護負擔與結構認知混淆。
- **根本原因**：專案演進初期由獨立 CLI 指令建立之預設根目錄直接搬移，未在早期進行全域架構扁平化。
- **解決方案**：
  - 徹底移除嵌套子資料夾 `midterm_drybean/` 與暫存交聯點，將 `src/`、`data/`、`output/`、`venv/`、`requirements.txt` 全數提升至 `04_期中專題_DryBean/` 主目錄。
  - 統一更新所有腳本、報告與投影片之相對路徑為原生 `output/figures/*.png`，消滅所有重複檔案與間接層級。
  - 經由實測驗證，全套腳本無縫執行，各項資源路徑 100% 直連成功。

---
*日誌維護者：Antigravity IDE Agentic Engine*  
*最新覆核時間：2026-10-13*
