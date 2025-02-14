// 下载功能相关的JavaScript代码
async function startDownload() {
    const urlInput = document.getElementById('url');
    const url = urlInput.value.trim();

    if (!url) {
        alert('请输入有效的YouTube URL');
        return;
    }

    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (response.ok) {
            alert('下载任务已添加到队列');
            urlInput.value = '';
        } else {
            alert(`错误: ${data.error}`);
        }
    } catch (error) {
        console.error('下载请求失败:', error);
        alert('下载请求失败，请稍后重试');
    }
}