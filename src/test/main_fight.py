# @Time: 2024年12月19日 22:04
# @Author: orcakill
# @File: main_fight.py
# @Description: 自动挑战

import os
import sys

from src.service.image_service import ImageService

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.windows_service import WindowsService
from src.utils.my_logger import my_logger as logger


def soul(game_devices: str):
    # 队员
    ComplexService.auto_setup(game_devices)
    for i in range(500):
        logger.debug("第{}次挑战", i + 1)
        ImageService.touch(Onmyoji.trials_arts_TZ, wait=4)
        ComplexService.fight_end(Onmyoji.trials_arts_ZDSL, Onmyoji.trials_arts_ZDSB, Onmyoji.trials_arts_ZCTZ,Onmyoji.trials_arts_TCTZ, 100, 2)



if __name__ == '__main__':
    WindowsService.limit_cpu_percentage(30)
    game_device = input("队员 请输入一个设备 0 云手机1 1 夜神模拟器 2 荣耀平板 3 小米手机 4云手机2：")
    soul(game_device)

