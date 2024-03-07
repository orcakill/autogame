# @Time: 2024年03月07日 09:46
# @Author: orcakill
# @File: test_mouse_service.py
# @Description: TODO
from unittest import TestCase

from src.service.mouse_service import MouseService


class MouseServiceTest(TestCase):
    @staticmethod
    def test_mouse_click():
        MouseService.mouse_click(hwnd="131740", pos1=(182, 110),wait_time=1)
