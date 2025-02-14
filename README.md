# MyMediaFactory

一个强大的媒体处理工具，支持YouTube视频下载和处理。

## 功能特点

- YouTube视频下载：支持多种格式和质量选项
- 视频格式转换（开发中）
- 语音转文字（开发中）

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/[your-username]/MyMediaFactory.git
cd MyMediaFactory
```

2. 安装后端依赖：
```bash
cd backend
pip install -r requirements.txt
```

3. 安装前端依赖：
```bash
cd frontend
npm install
```

## 使用说明

1. 启动后端服务：
```bash
cd backend
python server.py
```

2. 启动前端服务：
```bash
cd frontend
npm run dev
```

3. 打开浏览器访问：`http://localhost:3000`

## 技术栈

- 后端：Python, Flask
- 前端：Vue.js
- 视频处理：yt-dlp, FFmpeg
- 语音识别：Whisper

## 目录结构

```
- backend/          # 后端代码
  - core/           # 核心功能模块
  - server.py      # 主服务器
- frontend/        # 前端代码
- storage/         # 媒体文件存储
- tools/           # 工具和脚本
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License