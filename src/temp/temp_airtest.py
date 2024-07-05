import subprocess

import cv2
import numpy as np


def capture_screen():
    # 执行 scrcpy 命令进行屏幕捕获
    process = subprocess.Popen(['scrcpy'], stdout=subprocess.PIPE)

    # 读取捕获的图像数据
    image_data = process.stdout.read()

    # 将图像数据转换为 OpenCV 格式
    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    return image


if __name__ == "__main__":
    image = capture_screen()
    # 在此处对获取到的图像进行处理或保存
    cv2.imwrite('d:captured_image.jpg', image)
