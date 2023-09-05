# @Time: 2023年09月05日 11:57
# @Author: orcakill
# @File: temp_fight_end3.py
# @Description: 多线程，战斗结果识别


import threading
import time

from src.model.enum import Cvstrategy, Onmyoji
from src.service.image_service import ImageService
from src.utils.my_logger import logger

# 共享的中断标志
fight_interrupt_flag = False
# 战斗识别结果
fight_result = None


class ComplexService:
    @staticmethod
    def fight_end(fight_win: str, fight_fail: str, fight_again: str, fight_quit: str, fight_none: str = None,
                  timeouts: float = 60, timeout: float = 1):
        """
        结界战斗，结束战斗
        1、战斗胜利,退出挑战
        2、退出挑战
        3、再次挑战（只识别不点击），战斗失败
        :param timeouts: 识别最大时间
        :param fight_none: 挑战（挑战）
        :param timeout: 超时时间
        :param fight_win: 战斗胜利
        :param fight_fail: 战斗失败
        :param fight_again:  再次挑战
        :param fight_quit:  退出挑战
        :return:
        """
        global fight_interrupt_flag
        global fight_result
        fight_interrupt_flag = False
        fight_result = None
        # 创建线程1，战斗胜利，退出挑战
        thread1 = threading.Thread(target=ComplexService.fight_end_thread, name="fight-11",
                                   args=(fight_win, True, fight_quit, True, timeouts, timeout, True))
        # 创建线程2，退出挑战,无
        thread2 = threading.Thread(target=ComplexService.fight_end_thread, name="fight-12",
                                   args=(fight_quit, True, None, True, timeouts, timeout, True))
        # 创建线程3，再次挑战，战斗失败
        thread3 = threading.Thread(target=ComplexService.fight_end_thread, name="fight-13",
                                   args=(fight_again, False, fight_fail, True, timeouts, timeout))
        # 创建线程4，未挑战
        thread4 = threading.Thread(target=ComplexService.fight_end_thread, name="fight-14",
                                   args=(fight_none, False, None, True, timeouts, timeout))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        logger.debug("战斗结果:{}", fight_result)
        return fight_result

    @staticmethod
    def fight_end_thread(first, first_click, second, second_click, timeouts, timeout, again: bool = False):
        global fight_interrupt_flag
        global fight_result
        time_start = time.time()
        cvstrategy = Cvstrategy.sift
        rgb = False
        threshold = 0.7
        if first in [Onmyoji.border_GRJJ, Onmyoji.region_LJJ]:
            cvstrategy = Cvstrategy.default
        while time.time() - time_start < timeouts and not fight_interrupt_flag:
            is_first = ImageService.exists(first, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                           threshold=threshold, wait=timeout)
            if is_first and not fight_interrupt_flag:
                if first_click and again:
                    ImageService.exists(first, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb, threshold=threshold,
                                        is_click=True, wait=timeout)
                elif first_click and not again:
                    ImageService.touch_coordinate(is_first)
                fight_interrupt_flag = True
                fight_result = first
                if second is not None:
                    ImageService.exists(second, timeouts=timeout, is_click=second_click, wait=timeout)
                logger.debug("提前结束：{}", first)
                return True
        logger.debug("识别结束：{}", first)
        return False
