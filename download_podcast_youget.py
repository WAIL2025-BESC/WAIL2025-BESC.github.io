import os
import subprocess

# 设置下载目录
download_dir = 'documents/podcasts'
os.makedirs(download_dir, exist_ok=True)

# 要下载的播客URL
url = 'https://www.xiaoyuzhoufm.com/episode/66d1fae9e3b474d09ad97f99'

try:
    # 使用you-get下载
    print("开始下载播客...")
    subprocess.run(['you-get', '-o', download_dir, url], check=True)
    print(f"下载完成！文件保存在: {download_dir}")
    
except subprocess.CalledProcessError as e:
    print(f"下载出错: {e}")
except Exception as e:
    print(f"发生错误: {e}")