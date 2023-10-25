# @Time: 2023年08月07日 11:43
# @Author: orcakill
# @File: ocr_service.py
# @Description: 图像文字识别
import re

import pytesseract

from src.model.enum import Onmyoji
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

image_service = ImageService()
airtest_service = AirtestService()


class OcrService:
    @staticmethod
    def get_word(folder_path: str):
        """
        获取局部截图的文本或数字信息
        :param folder_path: 局部路径
        :return:
        """
        # 结界突破区域
        logger.debug("获取{}", folder_path)
        result = image_service.cv_match(folder_path)
        if result:
            pos1 = result['rectangle'][0]
            pos2 = result['rectangle'][2]
            # 截图
            img = airtest_service.crop_image(pos1[0], pos1[1], pos2[0], pos2[1])
            # 图像文字识别
            pil_image = airtest_service.cv2_2_pil(img)
            # pil_image.save("D:/a.png", quality=99, optimize=True)
            # image = Image.open('D:/a.png')
            # 打开图像
            image = pil_image.convert('RGBA')
            # 使用 Tesseract 进行文字识别
            text = pytesseract.image_to_string(image, lang='eng')
            if text:
                if folder_path == Onmyoji.border_JJTZJQY:
                    text = re.search(r'\d+(?=/30)', text)
                if folder_path == Onmyoji.friends_HYSQY:
                    text = re.search(r'\d+(?=/200)', text)
                if folder_path == Onmyoji.deed_MQSS:
                    text = re.search(r'\d+(?=/30)', text)
                if folder_path == Onmyoji.explore_DQLHSL:
                    text = re.search(r'\d+(?=/50)', text)
                if folder_path == Onmyoji.region_TZCS:
                    text = re.search(r'\d+(?=/6)', text)
            if text:
                text = text.group()
                text.replace(" ", "")
                logger.debug(text)
            else:
                logger.debug("无{}", folder_path)
            return text
            # 文字判断
        return None
