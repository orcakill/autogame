# @Time    : 2023年06月20日 15:17
# @Author  : orcakill
# @File    : test_image_service.py
# @Description : 图像识别测试类
import os

from airtest.core.helper import G

from src.model.enum import Onmyoji
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
import datetime

image_service = ImageService
airtest_service=AirtestService


def test_exists():
    airtest_service.auto_setup()
    now=datetime.datetime.now()
    screen = G.DEVICE.snapshot()
    now1 = datetime.datetime.now()
    print(now1-now)
