# @Time    : 2023年06月20日 15:17
# @Author  : orcakill
# @File    : test_image_service.py
# @Description : 图像识别测试类

import datetime

from src.model.enum import Onmyoji, Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService

image_service = ImageService
airtest_service = AirtestService


def test_exists():
    airtest_service.auto_setup("0")
    now = datetime.datetime.now()
    print(image_service.touch(Onmyoji.login_QHFWQ, cvstrategy=Cvstrategy.default))
    now1 = datetime.datetime.now()
    print(now1 - now)


def test_exists_coordinate():
    airtest_service.auto_setup("0")
    now = datetime.datetime.now()
    # 获取层字的横坐标，向下滑动3次
    test_coordinates = image_service.exists_coordinate(Onmyoji.soul_CZ,cvstrategy=Cvstrategy.default)
    print(test_coordinates)
    if  test_coordinates:
        x1=test_coordinates[0]
        y1=test_coordinates[1]
        x2=x1
        y2=2*y1
        airtest_service.swipe((x1,y1),(x2,y2))
    now1 = datetime.datetime.now()
    print(now1 - now)
