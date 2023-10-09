"""
# @Time: 2023年10月04日18:52
# @Author: orcakill
# @File: test_leveling.py
# @Description: 测试
"""
import time
from unittest import TestCase

from src.model.enum import Onmyoji, Cvstrategy
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.windows_service import WindowsService
from src.utils.my_logger import logger


class TestLeveling(TestCase):
    def test_plot(self):
        """
        剧情
        :return:
        """
        ImageService.auto_setup("2")
        for i in range(100):
            logger.debug("{}次", i + 1)
            logger.debug("三个点")
            ImageService.touch(Onmyoji.plot_SGD)
            logger.debug("下方跳过")
            ImageService.touch(Onmyoji.plot_XFTG)
            logger.debug("左侧聊天")
            ImageService.touch(Onmyoji.plot_ZCLT)
            logger.debug("灵视")
            ImageService.touch(Onmyoji.plot_LS)
            logger.debug("右上快进")
            ImageService.touch(Onmyoji.plot_XFTG, cvstrategy=Cvstrategy.default)
            logger.debug("小怪战斗")
            is_fight = ImageService.touch(Onmyoji.plot_XGZD)
            if is_fight:
                logger.debug("准备")
                ImageService.touch(Onmyoji.plot_ZB, wait=5)
                time.sleep(15)
            logger.debug("退出挑战")
            ImageService.touch(Onmyoji.plot_TCTZ)
            logger.debug("问号")
            ImageService.touch(Onmyoji.plot_WH)
            logger.debug("等待3s")
            time.sleep(3)

    def test_explore(self):
        WindowsService.limit_cpu_percentage(30)
        ImageService.auto_setup("2")
        # 战斗胜利次数
        num_win = 0
        # 战斗失败次数
        num_false = 0
        # 战斗用时列表
        time_fight_list = []
        logger.debug("探索测试-")
        # 获取设备分辨率
        resolution = ImageService.resolution_ratio()
        # 默认无boss
        is_boss = False
        is_little_monster = False
        for i_fight in range(1, 12):
            time_fight_start = time.time()
            logger.debug("探索测试-第{}次探索战斗", i_fight)
            if i_fight > 3:
                logger.debug("探索测试-点击首领")
                is_boss = ImageService.touch(Onmyoji.explore_SLZD)
            if not is_boss:
                logger.debug("探索测试-没有首领，点击小怪")
                for i_little_monster in range(2):
                    is_little_monster = ImageService.touch(Onmyoji.explore_XGZD)
                    if is_little_monster:
                        break
                    else:
                        logger.debug("探索测试-没有小怪,右移")
                        ImageService.swipe((0.9 * resolution[0], 0.5 * resolution[1]),
                                           (0.1 * resolution[0], 0.5 * resolution[1]))
                        logger.debug("探索测试-点击中心位置")
                        ImageService.touch_coordinate((0.5 * resolution[0], 0.6 * resolution[1]))
                        logger.debug("探索测试-进入下一轮循环")
                        continue
            if is_boss or is_little_monster:
                logger.debug("探索测试-等待战斗结果")
                is_result = ComplexService.fight_end(Onmyoji.explore_ZDSL, Onmyoji.explore_ZDSB, Onmyoji.explore_ZCTZ,
                                                     Onmyoji.explore_TCTZ, Onmyoji.explore_XGZD, None, 40, 2)
                if is_result in [Onmyoji.explore_ZDSL, Onmyoji.explore_TCTZ]:
                    logger.debug("探索测试-战斗胜利")
                    num_win = num_win + 1
                elif is_result in [Onmyoji.explore_ZCTZ, Onmyoji.explore_ZDSB]:
                    logger.debug("探索测试-失败")
                    num_false = num_false + 1
                time_fight_end = time.time()
                time_fight = time_fight_end - time_fight_start
                logger.debug("探索测试-本次探索-战斗结束，用时{}秒", round(time_fight, 3))
                time_fight_list.append(time_fight)
                if is_boss:
                    break
        logger.debug("探索测试-判断是否有式神录")
        is_reward = ImageService.exists(Onmyoji.explore_SSL, wait=4)
        if is_reward:
            logger.debug("探索测试-有式神录，点击左上角返回")
            ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
            logger.debug("探索测试-确认")
            ImageService.touch(Onmyoji.explore_QR)
        else:
            logger.debug("探索测试-无式神录")

    def test_call(self):
        WindowsService.limit_cpu_percentage(30)
        ImageService.auto_setup("1")
        logger.debug("开始")
        for i in range(100):
            logger.debug("{}次点击", i + 1)
            ImageService.touch(Onmyoji.call_ZCZH, timeouts=5, wait=5)
