# @Time: 2023年09月25日 15:49
# @Author: orcakill
# @File: main_team_1.py
# @Description: 双人合作
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.windows_service import WindowsService
from utils.my_logger import my_logger as logger


def soul_captain(game_devices: str):
    # 队长
    ComplexService.auto_setup(game_devices)
    for i in range(80):
        logger.debug("第{}次挑战", i + 1)
        is_fight = ImageService.touch(Onmyoji.soul_BQ_ZDTZ, wait=4)
        is_auto = ImageService.exists(Onmyoji.soul_BQ_ZD, timeouts=5)
        if not is_auto:
            is_fight = False
        # 无自动战斗，则重新点击挑战，拒接悬赏
        if not is_fight:
            ComplexService.refuse_reward()
            ImageService.touch(Onmyoji.soul_BQ_ZDTZ)
        ComplexService.fight_end_win(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ, 100, 2)


if __name__ == '__main__':
    WindowsService.limit_cpu_percentage(30)
    game_device = input("队长 请输入一个设备 0 云手机 1 夜神模拟器 2 荣耀平板 3 小米手机：")
    soul_captain(game_device)
