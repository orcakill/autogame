# @Time: 2023年08月07日 14:41
# @Author: orcakill
# @File: test_ocr_service.py
# @Description: 图像文字识别测试类
from unittest import TestCase

from src.service.airtest_service import AirtestService
from src.service.ocr_service import OcrService
from src.utils.my_logger import my_logger as logger

ocr_service = OcrService()
airtest_service = AirtestService()


class TestOcrService(TestCase):
    def test_border_bond(self):
        airtest_service.auto_setup("0")
        ocr_service.border_bond1()
        logger.debug("结束")
