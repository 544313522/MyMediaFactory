import yt_dlp
import os
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class VideoFormat:
    format_id: str
    ext: str
    resolution: str
    filesize: float
    format_note: str

@dataclass
class VideoInfo:
    title: str
    duration: int
    formats: List[VideoFormat]
    thumbnail: str
    description: str

class VideoDownloader:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.ydl_opts = {
            'format': 'best[ext=mp4]/best',  # 使用单一最佳格式，避免需要合并
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': False,
            'default_search': 'auto',
            'extract_flat': False
        }

    def get_video_info(self, url: str) -> Optional[VideoInfo]:
        """获取视频信息和可用的格式"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = []
                for f in info.get('formats', []):
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        formats.append(VideoFormat(
                            format_id=f['format_id'],
                            ext=f['ext'],
                            resolution=f.get('resolution', 'N/A'),
                            filesize=f.get('filesize', 0) / (1024 * 1024),  # Convert to MB
                            format_note=f.get('format_note', '')
                        ))

                return VideoInfo(
                    title=info['title'],
                    duration=info['duration'],
                    formats=formats,
                    thumbnail=info.get('thumbnail', ''),
                    description=info.get('description', '')
                )
        except Exception as e:
            print(f"获取视频信息失败: {str(e)}")
            return None

    def download_video(self, url: str, format_id: Optional[str] = None) -> bool:
        """下载视频
        
        Args:
            url: YouTube视频URL
            format_id: 可选的格式ID，如果不指定则使用最佳质量
            
        Returns:
            bool: 下载是否成功
        """
        try:
            opts = self.ydl_opts.copy()
            if format_id:
                opts['format'] = format_id

            with yt_dlp.YoutubeDL(opts) as ydl:
                print(f"开始下载视频: {url}")
                print(f"下载选项: {opts}")
                ydl.download([url])
            return True
        except yt_dlp.utils.DownloadError as e:
            print(f"下载视频失败 - 下载错误: {str(e)}")
            print(f"详细错误信息: {e.msg if hasattr(e, 'msg') else '未知错误'}")
            return False
        except yt_dlp.utils.ExtractorError as e:
            print(f"下载视频失败 - 提取器错误: {str(e)}")
            print(f"视频URL: {url}")
            return False
        except Exception as e:
            print(f"下载视频失败 - 未知错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            return False

    def _progress_hook(self, d: Dict):
        """下载进度回调"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f"下载进度: {percent} 速度: {speed}")
        elif d['status'] == 'finished':
            print(f"下载完成: {d['filename']}")