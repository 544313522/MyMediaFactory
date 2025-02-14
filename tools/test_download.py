import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core.youtube_engine.videodownloader import VideoDownloader

def test_download():
    # 初始化下载器
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage/input')
    downloader = VideoDownloader(output_dir)
    
    # 测试URL
    url = 'https://www.youtube.com/watch?v=ZLtXXFcHNOU'
    
    print('=== 开始下载测试 ===')
    print(f'输出目录: {output_dir}')
    print(f'测试URL: {url}')
    
    # 获取视频信息
    print('\n1. 获取视频信息...')
    info = downloader.get_video_info(url)
    if info:
        print(f'成功获取视频信息：')
        print(f'- 标题: {info.title}')
        print(f'- 时长: {info.duration}秒')
        print(f'- 可用格式数: {len(info.formats)}')
        
        # 尝试下载
        print('\n2. 开始下载视频...')
        success = downloader.download_video(url)
        print('下载结果：' + ('成功' if success else '失败'))
    else:
        print('无法获取视频信息')

if __name__ == '__main__':
    test_download()