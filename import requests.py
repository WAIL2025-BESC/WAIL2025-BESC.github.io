import requests
from bs4 import BeautifulSoup
import re
import os
import json

# 设置下载目录
download_dir = 'documents/podcasts'
os.makedirs(download_dir, exist_ok=True)

# 小宇宙播客URL
url = 'https://www.xiaoyuzhoufm.com/episode/66d1fae9e3b474d09ad97f99?s=eyJ1IjoiNjYxMGM2ODdlZGNlNjcxMDRhMDMxODg4In0%3D'

# 更新请求头，添加更多浏览器特征
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}

try:
    # 获取网页内容
    print("正在获取网页内容...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # 打印响应状态和内容长度
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容长度: {len(response.text)} 字节")
    
    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找包含音频信息的脚本标签
    scripts = soup.find_all('script')
    print(f"找到 {len(scripts)} 个脚本标签")
    
    audio_url = None
    episode_title = "对谈林亦LYi_AI应用"  # 默认标题
    
    # 保存响应内容以供调试
    with open('debug_response.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("已保存响应内容到 debug_response.html")
    
    for i, script in enumerate(scripts):
        if script.string and '__INITIAL_STATE__' in script.string:
            print(f"找到包含 __INITIAL_STATE__ 的脚本 (索引: {i})")
            json_str = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', script.string, re.DOTALL)
            if json_str:
                try:
                    data = json.loads(json_str.group(1))
                    if 'episode' in data and 'audios' in data['episode']:
                        audio_url = data['episode']['audios'][0]['url']
                        print(f"从JSON中提取到音频URL: {audio_url}")
                    if 'episode' in data and 'title' in data['episode']:
                        episode_title = data['episode']['title']
                        episode_title = re.sub(r'[\\/*?:"<>|]', '_', episode_title)
                        print(f"从JSON中提取到标题: {episode_title}")
                except json.JSONDecodeError as e:
                    print(f"JSON解析错误: {e}")
    
    if not audio_url:
        print("尝试查找audio标签...")
        audio_tags = soup.find_all('audio')
        print(f"找到 {len(audio_tags)} 个audio标签")
        for audio in audio_tags:
            if audio.get('src'):
                audio_url = audio.get('src')
                print(f"从audio标签找到URL: {audio_url}")
                break
    
    if audio_url:
        print(f"找到音频链接: {audio_url}")
        print(f"节目标题: {episode_title}")
        
        print("开始下载音频文件...")
        audio_response = requests.get(audio_url, headers=headers, stream=True)
        audio_response.raise_for_status()
        
        content_type = audio_response.headers.get('Content-Type', '')
        print(f"音频文件类型: {content_type}")
        
        ext = 'mp3'  # 默认扩展名
        if 'mpeg' in content_type or 'mp3' in content_type:
            ext = 'mp3'
        elif 'mp4' in content_type:
            ext = 'mp4'
        
        file_path = os.path.join(download_dir, f"{episode_title}.{ext}")
        print(f"正在保存到: {file_path}")
        
        with open(file_path, 'wb') as f:
            for chunk in audio_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"音频已成功下载到: {file_path}")
    else:
        print("未找到音频链接")
        print("可能原因:")
        print("1. 网页需要JavaScript渲染")
        print("2. 需要登录或认证")
        print("3. 内容受保护")
        print("请检查 debug_response.html 文件了解更多信息")
        
except Exception as e:
    print(f"下载过程中出错: {e}")