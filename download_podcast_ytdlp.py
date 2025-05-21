import os
import subprocess

# 设置下载目录
download_dir = 'documents/podcasts'
os.makedirs(download_dir, exist_ok=True)

# 要下载的播客URL
url = 'https://caifuhao.eastmoney.com/news/20250430232713017448860'

try:
    # 使用yt-dlp下载
    print("开始下载播客...")
    subprocess.run([
        'yt-dlp',
        '-o', os.path.join(download_dir, '%(title)s.%(ext)s'),
        '--extract-audio',
        '--audio-format', 'mp3',
        url
    ], check=True)
    print(f"下载完成！文件保存在: {download_dir}")
    
except subprocess.CalledProcessError as e:
    print(f"下载出错: {e}")
except Exception as e:
    print(f"发生错误: {e}")