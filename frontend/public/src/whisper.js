// AI转写功能相关的JavaScript代码
async function startTranscription() {
    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('请选择要转写的音频或视频文件');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/transcribe', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            alert('转写任务已添加到队列');
            fileInput.value = '';
        } else {
            alert(`错误: ${data.error}`);
        }
    } catch (error) {
        console.error('转写请求失败:', error);
        alert('转写请求失败，请稍后重试');
    }
}