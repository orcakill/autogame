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
    def border_bond():
        # 获取左上角图片
        # 结界首页，用于获取纵坐标
        pos1 = image_service.exists(Onmyoji.border_JJSY)
        # 右上角突破，用于获取横坐标
        pos2 = image_service.exists(Onmyoji.border_YSJTP)
        if pos1 and pos2:
            # 获取设备分辨率
            pos3 = airtest_service.resolving_power()
            # 截图
            img = airtest_service.crop_image(pos2[0] + 10, 0, pos3[0], pos1[1])
            # 图像文字识别
            pil_image = airtest_service.cv2_2_pil(img)
            # pil_image.save("D:/score0.png", quality=99, optimize=True)
            # 打开图像
            image = pil_image.convert('RGBA')

            # 使用 Tesseract 进行文字识别
            text = pytesseract.image_to_string(image, lang='eng').replace(" ", "").replace(":", "").replace("<", "")
            result = re.sub(r'\D', '', text)
            logger.debug(result)
            if result == "030":
                return True
            # 文字判断
        return False
