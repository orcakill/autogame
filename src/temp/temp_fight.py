# @Time: 2025年03月02日 23:35
# @Author: orcakill
# @File: temp_fight.py
# @Description: 临时挑战
import time

from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import my_logger as logger


def soul(game_devices: str):
    # 队员
    ComplexService.auto_setup(game_devices)
    for i in range(5):
        for j in range(10):
            logger.debug("第{}次等待战斗结果", i + 1)
            ImageService.touch(Onmyoji.soul_BQ_TZLS, wait=4)
            ComplexService.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB, Onmyoji.soul_BQ_ZCTZ,
                                     Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_TZLS, None, 30, 1)
        time.sleep(10)


def ghost_king(game_devices: str):
    ComplexService.auto_setup(game_devices)
    for i in range(5):
        for j in range(10):
            logger.debug("第{},{}次战斗", i + 1, j + 1)
            # 召唤鬼王
            logger.debug("召唤鬼王")
            is_1=ImageService.exists(Onmyoji.temp_super_ZHGW)
            if is_1:
                ImageService.exists(Onmyoji.temp_super_ZHGW, wait=4,is_click=True)
                time.sleep(4)
                # 挑战
            logger.debug("挑战")
            is_2=ImageService.exists(Onmyoji.temp_super_TZ)
            if is_2:
                ImageService.exists(Onmyoji.temp_super_TZ, wait=4,is_click=True)
                time.sleep(4)
            # 准备
            logger.debug("准备")
            is_3=ImageService.exists(Onmyoji.temp_super_ZB)
            if is_3:
                ImageService.exists(Onmyoji.temp_super_ZB, wait=4,is_click=True)
                time.sleep(20)
                # 胜利
            logger.debug("战斗胜利")
            is_4 = ImageService.exists(Onmyoji.temp_super_ZDSL)
            if is_4:
                ImageService.exists(Onmyoji.temp_super_ZDSL, wait=4, is_click=True)
        time.sleep(10)


if __name__ == '__main__':
    # 2 荣耀平板
    ghost_king("2")
