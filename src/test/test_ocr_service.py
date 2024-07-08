# @Time: 2023年08月07日 14:41
# @Author: orcakill
# @File: test_ocr_service.py
# @Description: 图像文字识别测试类
from unittest import TestCase

from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.utils.my_logger import my_logger as logger


class TestOcrService(TestCase):
    def test_border_bond(self):
        ComplexService.auto_setup("1")
        result = OcrService.get_word(Onmyoji.explore_DQLHSL, lang='chi_sim')
        logger.debug(result)
        logger.debug("结束")

    @staticmethod
    def test_ocr():
        ComplexService.auto_setup("1")
        ImageService.ocr_touch("切换")
        logger.debug("结束")
