# -*- coding: utf-8 -*-
"""
push_to_github.py: 自動將專案推送到指定的 GitHub 倉庫
支援格式：
    python push_to_github.py https://github.com/USERNAME/REPO.git [GITHUB_TOKEN]
"""
import sys
import os
import dulwich.porcelain as p

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    if len(sys.argv) < 2:
        print("【提示】請提供遠端 GitHub 倉庫 URL！")
        print("語法範例：python push_to_github.py https://github.com/username/repo_name.git [GITHUB_TOKEN]")
        return

    repo_url = sys.argv[1].strip()
    token = sys.argv[2].strip() if len(sys.argv) > 2 else None

    # 若傳入 Token 且未於 URL 中攜帶認證資訊，則自動構建含憑證的 HTTPS 網址
    if token and "https://" in repo_url and "@" not in repo_url:
        clean_url = repo_url.replace("https://", "")
        repo_url = f"https://oauth2:{token}@{clean_url}"

    # 錨定至工作區根目錄（含有 .git 的位置）
    # 腳本位於 04_期中專題_DryBean/src/，上兩層為根目錄
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    display_target = repo_url.split('@')[-1] if '@' in repo_url else repo_url
    print(f"==================================================")
    print(f"正在連線並上傳至 GitHub: https://{display_target}...")
    print(f"目標分支: main")
    print(f"==================================================")

    # 儲存到 config 的遠端網址保持乾淨（不包含 Token 密碼）
    clean_target_url = f"https://{clean_url}" if token and "@" not in sys.argv[1] else sys.argv[1]
    try:
        p.remote_add(ROOT_DIR, 'origin', clean_target_url.encode('utf-8'))
        print("已新增遠端倉庫 (origin)")
    except Exception:
        # remote 已存在時嘗試更新
        try:
            repo = p.open_repo_closing(ROOT_DIR)
            c = repo.get_config()
            c.set((b'remote', b'origin'), b'url', clean_target_url.encode('utf-8'))
            c.write_to_path()
            print("已更新遠端倉庫 (origin) 網址")
        except Exception:
            pass

    try:
        p.push(ROOT_DIR, repo_url, refspecs=[b'refs/heads/main:refs/heads/main'], force=True)
        print("==================================================")
        print("🎉 上傳成功！全體專案檔案已完整推送至 GitHub！")
        print("==================================================")
    except Exception as e:
        print(f"❌ 上傳失敗: {e}")
        print("【排錯建議】")
        print("1. 請確認該 GitHub 倉庫是否已在 github.com 建立。")
        print("2. 若為私有倉庫 (Private)，請提供 GitHub Personal Access Token (PAT)。")
        print("3. 若倉庫已有內容，可能需要 force push 或先確認權限。")

if __name__ == '__main__':
    main()
