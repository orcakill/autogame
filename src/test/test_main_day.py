# @Time: 2024年01月14日 15:24
# @Author: orcakill
# @File: test_main.py
# @Description: TODO
from unittest import TestCase

from src.controller.onmyoji_controller import OnmyojiController


class TestMainDay(TestCase):

    def test_initialization1(self):
        OnmyojiController.create_execute_tasks("0", '1', project_name="登录",
                                               start_hour=0, end_hour=23)

    def test_initialization2(self):
        OnmyojiController.create_execute_tasks("4", '2', project_name="登录",
                                               start_hour=0, end_hour=23)
