from typing import Union
import cv2
import numpy as np
from PIL import Image
from src.model.enum import Onmyoji
from src.service.image_service import ImageService
from src.utils.my_logger import my_logger as logger

def find_picture_identify_work_po_list(original_image, template_image_list, coefficient, characteristic_point, print_or_not):
    # 声明坐标列表
    mouse_messages = []
    # 特征匹配
    sift = cv2.SIFT_create()
    original_image_array = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    key_points_original, descriptors_original = sift.detectAndCompute(original_image_array, None)

    for template_image in template_image_list:
        try:
            image2: Union[Image.Image, np.ndarray] = Image.open(template_image.filename)
            image2 = np.asarray(image2)
            template_image_array = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
            key_points_template, descriptors_template = sift.detectAndCompute(template_image_array, None)

            # 使用FLANN匹配器
            flann = cv2.FlannBasedMatcher()
            matches = flann.knnMatch(descriptors_template, descriptors_original, k=2)

            # 选择良好的匹配点
            good_matches = []
            for m, n in matches:
                if m.distance < coefficient * n.distance:
                    good_matches.append(m)

            # 当匹配后的特征点大于等于4个，则认为模板图在原图中
            if len(good_matches) >= characteristic_point:
                template_points = np.float32([key_points_template[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                original_points = np.float32([key_points_original[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

                # 使用findHomography计算透视变换矩阵
                M, mask = cv2.findHomography(template_points, original_points, cv2.RANSAC, 3)

                # 获取模板图像的尺寸
                h, w = template_image_array.shape

                # 计算模板图像的四个顶点
                template_corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)

                # 使用透视变换矩阵对模板图像的四个顶点进行变换
                transformed_corners = cv2.perspectiveTransform(template_corners, M)

                # 计算包围矩形的坐标
                x, y, w, h = cv2.boundingRect(transformed_corners)

                if x >= 0 and y >= 0:
                    picture_identify_work_po = {
                        'x': int(x + w / 2),
                        'y': int(y + h / 2)
                    }

                    if print_or_not:
                        # 在原图上绘制矩形
                        cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.imwrite('D:/match.jpg', original_image)

                    print(f"目标坐标为: ({picture_identify_work_po['x']}, {picture_identify_work_po['y']})")
                    mouse_messages.append(picture_identify_work_po)

                    if len(mouse_messages) > 1:
                        return mouse_messages

        except Exception as e:
            logger.exception(e)

    return mouse_messages

if __name__ == '__main__':
    # 读取本地图片
    image1: Union[Image.Image, np.ndarray] = Image.open('D://a.png')
    image1 = np.asarray(image1)

    # 读取本地文件夹
    template_list = ImageService.get_template_list(Onmyoji.border_GRJJWZB, True, 0.7)
    find_picture_identify_work_po_list(image1, template_list, 0.7, 4, True)