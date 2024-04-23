# @Time: 2023年09月25日 15:49
# @Author: orcakill
# @File: main_team_1.py
# @Description: 双人合作
import os
import sys

from src.controller.onmyoji_controller import OnmyojiController

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.windows_service import WindowsService
from utils.my_logger import my_logger as logger


def soul2(game_devices: str):
    # 队员
    ComplexService.auto_setup(game_devices)
    for i in range(80):
        logger.debug("第{}次等待战斗结果", i + 1)
        ComplexService.fight_end_win(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ, 100, 2)


if __name__ == '__main__':
    WindowsService.limit_cpu_percentage(30)
    game_device = input("队员 请输入一个设备 0 云手机 1 夜神模拟器 2 荣耀平板 3 小米手机：")
    soul2(game_device)


