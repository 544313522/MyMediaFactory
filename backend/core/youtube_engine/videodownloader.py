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
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = []
                best_formats = {}  # 用于存储每个分辨率的最佳格式
                
                # 首先收集所有格式
                for f in info.get('formats', []):
                    if f.get('vcodec') != 'none':
                        height = f.get('height', 0)
                        if height:
                            current_size = f.get('filesize', 0) or 0  # 如果filesize为None则使用0
                            if height not in best_formats:
                                best_formats[height] = f
                            else:
                                existing_size = best_formats[height].get('filesize', 0) or 0
                                if current_size > existing_size:
                                    best_formats[height] = f
                
                # 按分辨率从高到低排序
                for height in sorted(best_formats.keys(), reverse=True):
                    f = best_formats[height]
                    filesize = f.get('filesize', 0) or 0  # 如果filesize为None则使用0
                    formats.append(VideoFormat(
                        format_id=f['format_id'],
                        ext=f['ext'],
                        resolution=f"{height}p",
                        filesize=filesize / (1024 * 1024),  # 转换为MB
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

    def download_video(self, url: str, format_id: str) -> bool:
        try:
            opts = self.ydl_opts.copy()
            
            if format_id == 'audio-only':
                opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                })
            elif format_id == 'subtitles-only':
                opts.update({
                    'skip_download': True,
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': ['zh-Hans', 'en']  # 下载中文和英文字幕
                })
            else:
                opts['format'] = format_id

            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"下载失败: {str(e)}")
            return False

    def download_video(self, url: str, format_id: str = None) -> bool:
        try:
            opts = self.ydl_opts.copy()
            
            if format_id == 'audio-only':
                opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                })
            elif format_id == 'subtitles-only':
                opts.update({
                    'skip_download': True,
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': ['zh-Hans', 'en']
                })
            else:
                # 使用指定的格式ID
                opts['format'] = format_id
            
            print(f"下载选项: {opts}")  # 调试信息
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"下载失败: {str(e)}")
            return False

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

    def download_video(self, url: str, options: dict) -> bool:
        try:
            format_id = options.get('format_id', '')
            want_audio = options.get('audio', False)
            want_subtitle = options.get('subtitle', False)
            
            # 基础配置
            opts = {
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
            }
    
            # 设置下载格式
            if not format_id and want_audio and not want_subtitle:
                # 仅下载音频
                opts.update({
                    'format': 'bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                })
            elif not format_id and not want_audio and want_subtitle:
                # 仅下载字幕
                opts.update({
                    'skip_download': True,
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': ['zh-Hans', 'en']
                })
            else:
                # 下载视频（可能带字幕和音频）
                if format_id:
                    opts['format'] = format_id
                else:
                    opts['format'] = 'best'
    
                # 添加字幕下载选项
                if want_subtitle:
                    opts['writesubtitles'] = True
                    opts['writeautomaticsub'] = True
                    opts['subtitleslangs'] = ['zh-Hans', 'en']
    
                # 如果需要额外的音频文件
                if want_audio:
                    if 'postprocessors' not in opts:
                        opts['postprocessors'] = []
                    opts['postprocessors'].append({
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    })
    
            print(f"使用的下载选项: {opts}")  # 调试日志
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"下载失败: {str(e)}")
            print(f"错误类型: {type(e)}")
            import traceback
            print(f"详细错误: {traceback.format_exc()}")
            return False

    def _progress_hook(self, d: Dict):
        """下载进度回调"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f"下载进度: {percent} 速度: {speed}")
        elif d['status'] == 'finished':
            print(f"下载完成: {d['filename']}")