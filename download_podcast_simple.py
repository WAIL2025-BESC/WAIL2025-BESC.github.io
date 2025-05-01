from xyzfm import XYZ
import os

# 设置下载目录
download_dir = 'documents/podcasts'
os.makedirs(download_dir, exist_ok=True)

# 创建XYZ实例
xyz = XYZ()

# 要下载的播客URL或ID
episode_id = '66d1fae9e3b474d09ad97f99'

try:
    # 下载音频
    print("开始下载播客...")
    xyz.download_audio(episode_id, download_dir)
    print(f"下载完成！文件保存在: {download_dir}")
    
except Exception as e:
    print(f"下载出错: {e}")