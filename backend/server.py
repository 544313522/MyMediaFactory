from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from config import SERVER_HOST, SERVER_PORT, STORAGE_CONFIG
from core.youtube_engine.videodownloader import VideoDownloader

app = Flask(__name__, static_folder='../frontend/public', static_url_path='/')

# 初始化下载器
downloader = VideoDownloader(STORAGE_CONFIG['INPUT_DIR'])

@app.route('/')
def index():
    return app.send_static_file('index.html')

# 确保存储目录存在
for dir_path in STORAGE_CONFIG.values():
    os.makedirs(dir_path, exist_ok=True)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': '请提供有效的URL'}), 400
    
    try:
        # 获取视频信息
        video_info = downloader.get_video_info(url)
        if not video_info:
            return jsonify({'error': '无法获取视频信息'}), 400

        # 开始下载视频
        success = downloader.download_video(url)
        if success:
            return jsonify({
                'message': '下载成功',
                'title': video_info.title if video_info else 'Unknown'
            })
        else:
            return jsonify({'error': '下载失败'}), 500
    except Exception as e:
        return jsonify({'error': f'下载过程出错: {str(e)}'}), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
        
    filename = secure_filename(file.filename)
    file_path = os.path.join(STORAGE_CONFIG['INPUT_DIR'], filename)
    file.save(file_path)
    
    # TODO: 将转写任务添加到队列
    return jsonify({'message': '任务已添加到队列'})

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)