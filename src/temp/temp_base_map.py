# @Time: 2024年06月18日 09:46
# @Author: orcakill
# @File: temp_base_map.py
# @Description: 去除底图
import numpy as np
from skimage import data
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from skimage.segmentation import slic


def base_map():
    # 读取图像
    image = imread('D:\\a.png')
    # 转换为灰度图像
    gray_image = rgb2gray(image)
    # 使用SLIC算法进行图像分割
    segments = slic(image, n_segments=100, compactness=10)
    # 创建一个与原始图像相同大小的掩码，用于标记分割结果
    mask = np.zeros_like(image)
    # 根据分割结果为每个区域赋予不同的颜色
    for label in np.unique(segments):
        mask[segments == label] = np.random.randint(0, 255, 3)
    # 保存分割结果
    imsave('D:\\b.png', mask)


if __name__ == '__main__':
    base_map()
