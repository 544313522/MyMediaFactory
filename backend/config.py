# 配置文件

# 服务器配置
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# 存储路径配置
STORAGE_CONFIG = {
    'INPUT_DIR': 'storage/input',
    'PROCESSING_DIR': 'storage/processing',
    'OUTPUT_DIR': 'storage/output'
}

# YouTube下载器配置
YOUTUBE_DL_CONFIG = {
    'FORMAT': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'SUBTITLES': True,
    'COOKIES_FILE': None
}

# Whisper AI配置
WHISPER_CONFIG = {
    'MODEL': 'base',  # 可选: tiny, base, small, medium, large
    'LANGUAGE': 'auto',
    'TASK': 'transcribe'
}

# 队列配置
QUEUE_CONFIG = {
    'MAX_WORKERS': 2,
    'TIMEOUT': 3600  # 任务超时时间（秒）
}