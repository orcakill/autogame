# @Time: 2023年08月05日 15:48
# @Author: orcakill
# @File: test_complex_service.py
# @Description: TODO
import datetime
from unittest import TestCase

from src.model.enum import Onmyoji
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

image_service = ImageService
airtest_service = AirtestService
complex_service = ComplexService


class TestComplexService(TestCase):
    def test_broder_fight_end(self):
        airtest_service.auto_setup("0")
        logger.debug("开始")
        now = datetime.datetime.now()
        complex_service.broder_fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB, Onmyoji.border_ZCTZ,
                                         Onmyoji.border_TCTZ, 60)

        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)
