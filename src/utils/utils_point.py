# @Time: 2025年02月19日 09:01
# @Author: orcakill
# @File: utils_point.py
# @Description: 特征点检查
import os

import cv2
import numpy as np

from src.model.enum import Onmyoji
from src.utils.my_logger import my_logger as logger
from src.utils.utils_path import UtilsPath


def detect_keypoints(image_path, min_points=4):
    """
    检测图像中的特征点，并检查是否满足最小数量要求。

    :param image_path: 图像文件路径（支持 PNG 格式）
    :param min_points: 所需的最小特征点数量，默认为 4
    :return: 如果特征点数量足够返回 True，否则返回 False
    """
    # 读取图像
    # 以二进制模式读取文件
    with open(image_path, 'rb') as f:
        buffer = f.read()
    # 将二进制数据转换为 numpy 数组
    image_array = np.frombuffer(buffer, dtype=np.uint8)
    # 解码图像
    image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)


    if image is None:
        logger.debug(f"不能获取{image_path}")
        return False

    # 初始化特征检测器（这里使用 ORB 作为示例）
    detector = cv2.SIFT_create()

    # 检测特征点
    keypoints = detector.detect(image, None)

    # 检查特征点数量
    if len(keypoints) < min_points:
        logger.error(f"图片{image_path}特征点少于{min_points}，实际特征点{len(keypoints)}")
        return True
    else:
        # logger.debug(f"图片{image_path}实际特征点{len(keypoints)}")
        return False


if __name__ == '__main__':
    folder_path = str('')
    folder_all_path = os.path.join(UtilsPath.get_onmyoji_image_path(), folder_path)
    for root, dirs, files in os.walk(folder_all_path):
        for file_name in files:
            file_path = os.path.abspath(os.path.join(root, file_name))
            # 判断文件是否是图片类型
            file_ext = file_path.split('.')[-1].lower()
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                detect_keypoints(file_path)
