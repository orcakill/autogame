# @Time: 2024年06月19日 15:26
# @Author: orcakill
# @File: impl_ocr.py
# @Description: 图像文字识别
from src.service.airtest_service import AirtestService
from src.service.ocr_service import OcrService


class ImplOcr:
    @staticmethod
    def ocr_touch(word):
        # 获取当前图片
        screen = AirtestService.snapshot()
        # 获取文字坐标
        pos = OcrService.ocr_paddle(screen, word)
        # 点击
        AirtestService.touch_coordinate(pos)
