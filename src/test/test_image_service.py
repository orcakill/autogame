# @Time    : 2023年06月20日 15:17
# @Author  : orcakill
# @File    : test_image_service.py
# @Description : 图像识别测试类

import datetime
from unittest import TestCase

from src.model.enum import Onmyoji, Cvstrategy
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger

image_service = ImageService
complex_service = ComplexService
ocr_service = OcrService


class TestImageService(TestCase):
    def test_exists(self):
        image_service.auto_setup("0")
        now = datetime.datetime.now()
        is_border = ImageService.touch(Onmyoji.shack_MZ,cvstrategy=Cvstrategy.default)
        logger.debug(is_border)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_exists_coordinate(self):
        image_service.auto_setup("0")
        now = datetime.datetime.now()
        complex_service.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                  Onmyoji.border_ZCTZ, Onmyoji.home_TS, Onmyoji.border_GRJJ, 60, 1)
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_touch(self):
        image_service.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        ImageService.exists(Onmyoji.home_DBCDDK)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_snapshot(self):
        image_service.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        image_service.snapshot("1")
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_crop_image(self):
        image_service.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        image_service.crop_image(100, 100, 200, 200)
        logger.debug("结束")
        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_faster(self):
        image_service.auto_setup("0")
        logger.debug("循环识别测试")
        now = datetime.datetime.now()
        target_card = False
        # 获取设备分辨率
        resolution = image_service.resolving_power()
        target_type = None
        for i_type in range(1, 8):
            if i_type == 1:
                target_card = Onmyoji.foster_JJK_LXTG
                target_type = Onmyoji.foster_JJK_TG
            elif i_type == 2:
                target_card = Onmyoji.foster_JJK_WXTG
                target_type = Onmyoji.foster_JJK_TG
            elif i_type == 3:
                target_type = Onmyoji.foster_JJK_TG
                target_card = Onmyoji.foster_JJK_SXTG1
            elif i_type == 4:
                target_type = Onmyoji.foster_JJK_DY
                target_card = Onmyoji.foster_JJK_LXDY
            elif i_type == 5:
                target_type = Onmyoji.foster_JJK_DY
                target_card = Onmyoji.foster_JJK_WXDY
            elif i_type == 6:
                target_type = Onmyoji.foster_JJK_TG
                target_card = Onmyoji.foster_JJK_SXTG
            elif i_type == 7:
                target_type = Onmyoji.foster_JJK_DY
                target_card = Onmyoji.foster_JJK_SXDY1
            type1 = image_service.exists(target_type, threshold=0.8)
            if type1:
                result = image_service.exists(target_card, threshold=0.8)
                if result and result[0] < 1 / 2 * resolution[0]:
                    result = False
                logger.debug("{}：{}", target_card, result)

        now1 = datetime.datetime.now()
        print(now1 - now)

    def test_find_all(self):
        """
        多图查找
        :return:
        """

        image_service.auto_setup("0")
        now = datetime.datetime.now()
        # 测试代码
        logger.debug("开始")
        result = image_service.find_all(Onmyoji.region_GP)
        logger.debug(result)
        logger.debug(len(result))
        logger.debug("结束")
        now1 = datetime.datetime.now()
        logger.debug(now1 - now)
