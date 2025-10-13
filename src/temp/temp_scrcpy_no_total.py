import subprocess
import cv2
import numpy as np


def capture_via_scrcpy_headless():
    # 启动 scrcpy 无头模式并获取视频流
    cmd = [
        'scrcpy',
        '--no-playback"',
        '--max-size', '800',  # 限制分辨率提高性能
        '--max-fps', '30',
        '--output', 'tcp://127.0.0.1:8000'  # 输出到TCP端口
    ]

    process = subprocess.Popen(cmd)

    # 连接到视频流并捕获帧
    cap = cv2.VideoCapture('tcp://127.0.0.1:8000')
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('screenshot.png', frame)

    cap.release()
    process.terminate()
    return frame

if __name__ == '__main__':
     capture_via_scrcpy_headless()
