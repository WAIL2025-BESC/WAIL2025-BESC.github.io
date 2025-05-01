import requests
import json
import os

# 设置下载目录
download_dir = 'documents/podcasts'
os.makedirs(download_dir, exist_ok=True)

# API URL
api_url = 'https://api.xiaoyuzhoufm.com/v1/episode/66d1fae9e3b474d09ad97f99'

# 设置请求头，添加认证信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Origin': 'https://www.xiaoyuzhoufm.com',
    'Referer': 'https://www.xiaoyuzhoufm.com/',
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN_HERE'  # 需要添加有效的访问令牌
}

try:
    # 获取音频信息
    print("正在获取音频信息...")
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    print(f"API响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    # 从响应中提取音频URL
    if 'audio_url' in data:
        audio_url = data['audio_url']
        print(f"找到音频链接: {audio_url}")
        
        # 下载音频文件
        print("开始下载音频文件...")
        audio_response = requests.get(audio_url, headers=headers, stream=True)
        audio_response.raise_for_status()
        
        # 保存文件
        file_path = os.path.join(download_dir, "podcast.mp3")
        total_size = int(audio_response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        
        with open(file_path, 'wb') as f:
            for chunk in audio_response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    percentage = int((downloaded / total_size) * 100)
                    print(f"\r下载进度: {percentage}%", end='')
        
        print(f"\n音频已成功下载到: {file_path}")
    else:
        print("未找到音频链接")
        print("API响应中没有找到音频URL")

except requests.exceptions.HTTPError as e:
    print(f"HTTP错误: {e}")
    if e.response.status_code == 401:
        print("认证失败：需要有效的访问令牌")
        print("请先登录小宇宙网站并获取有效的访问令牌")
except Exception as e:
    print(f"下载过程中出错: {e}")