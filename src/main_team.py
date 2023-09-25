# @Time: 2023年09月25日 15:49
# @Author: orcakill
# @File: main_team.py
# @Description: 双人合作
from src.model.enum import Onmyoji
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from utils.my_logger import my_logger as logger


def soul1(game_devices: str):
    # 队长
    ImageService.auto_setup(game_devices)
    for i in range(80):
        logger.debug("第{}次挑战", i + 1)
        is_fight = ImageService.touch(Onmyoji.soul_BQ_TZ)
        if not is_fight:
            ComplexService.refuse_reward()
            logger.debug("点击可能的准备")
            ImageService.touch(Onmyoji.soul_BQ_ZB)
        ComplexService.fight_end(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_ZDSB, Onmyoji.soul_BQ_ZCTZ,
                                 Onmyoji.soul_BQ_TCTZ, Onmyoji.soul_BQ_TZ, None, 100, 1)


def soul2(game_devices: str):
    # 队员
    ImageService.auto_setup(game_devices)
    for i in range(80):
        logger.debug("第{}次等待战斗结果", i + 1)
        ComplexService.fight_end_win(Onmyoji.soul_BQ_ZDSL, Onmyoji.soul_BQ_TCTZ, 100, 1)


if __name__ == '__main__':
    game_type = input("请输入一个身份，1 队长 2队员：")
    game_device = input("请输入一个设备 0 云手机 1 夜神模拟器 2 荣耀平板 3 小米手机：")
    if game_type == '1':
        soul1(game_device)
    else:
        soul2(game_device)
