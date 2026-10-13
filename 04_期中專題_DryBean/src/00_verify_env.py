import sys
import importlib

packages = [
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "sklearn",
    "openpyxl",
    "requests"
]

print("==========================================")
print("Python Environment Verification")
print("==========================================")
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version.split()[0]}")
print("------------------------------------------")

all_ok = True
for pkg in packages:
    try:
        mod = importlib.import_module(pkg)
        ver = getattr(mod, "__version__", "OK")
        print(f"  [OK] {pkg:15s}: {ver}")
    except ImportError as e:
        print(f"  [FAIL] {pkg:15s}: NOT FOUND ({e})")
        all_ok = False

print("------------------------------------------")
if all_ok:
    print("Verification SUCCESS: All required modules are installed!")
else:
    print("Verification FAILED: Some packages are missing.")
print("==========================================")
