// 下载功能相关的JavaScript代码
async function startDownload() {
    const url = document.getElementById('url').value.trim();
    const formatSelect = document.getElementById('format-select');
    const downloadSubtitle = document.getElementById('download-subtitle').checked;
    
    if (!url) {
        alert('请输入视频URL');
        return;
    }
    
    // 如果既没有选择视频格式也没有选择字幕，提示用户
    if (!formatSelect.value && !downloadSubtitle) {
        alert('请选择下载内容（视频格式或字幕）');
        return;
    }

    try {
        console.log('开始下载，参数:', {
            url: url,
            format_id: formatSelect.value,
            subtitle: downloadSubtitle
        });

        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                options: {
                    format_id: formatSelect.value,
                    subtitle: downloadSubtitle
                }
            })
        });

        const data = await response.json();
        if (response.ok) {
            alert('开始下载，请等待完成');
        } else {
            alert(`错误: ${data.error}`);
        }
    } catch (error) {
        console.error('下载请求失败:', error);
        alert('下载请求失败，请稍后重试');
    }
}

// 添加测试函数
function testConnection() {
    console.log('JavaScript 已加载');
}

// 立即执行测试
testConnection();

async function getVideoInfo() {
    const urlInput = document.getElementById('url');
    const getInfoButton = document.querySelector('#downloader button');
    const url = urlInput.value.trim();

    if (!url) {
        alert('请输入视频URL');
        return;
    }

    try {
        // 显示加载状态
        getInfoButton.textContent = '正在获取信息...';
        getInfoButton.disabled = true;

        const response = await fetch('/api/video-info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();
        if (response.ok) {
            displayVideoInfo(data);
        } else {
            alert(`错误: ${data.error}`);
        }
    } catch (error) {
        console.error('获取视频信息失败:', error);
        alert('获取视频信息失败，请稍后重试');
    } finally {
        // 恢复按钮状态
        getInfoButton.textContent = '获取视频信息';
        getInfoButton.disabled = false;
    }
}

function displayVideoInfo(info) {
    console.log('显示视频信息:', info); // 调试日志
    const videoInfo = document.getElementById('video-info');
    const title = document.getElementById('video-title');
    const thumbnail = document.getElementById('video-thumbnail');
    const formatSelect = document.getElementById('format-select');

    if (!videoInfo || !title || !thumbnail || !formatSelect) {
        console.error('找不到必要的 DOM 元素');
        return;
    }

    // 设置视频标题和缩略图
    title.textContent = info.title;
    thumbnail.src = info.thumbnail;

    // 清空并填充格式选项
    formatSelect.innerHTML = '<option value="">选择清晰度...</option>';
    
    // 添加视频格式选项
    if (info.formats && Array.isArray(info.formats)) {
        info.formats.forEach(format => {
            const option = document.createElement('option');
            option.value = format.format_id;
            const size = format.filesize ? `(${(format.filesize).toFixed(1)}MB)` : '';
            option.textContent = `${format.resolution} - ${format.format_note} ${size}`;
            formatSelect.appendChild(option);
        });
    }

    // 显示视频信息区域
    videoInfo.style.display = 'block';
}