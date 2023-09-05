# @Time: 2023年08月04日 18:27
# @Author: orcakill
# @File: complex_service.py
# @Description: 复杂逻辑处理
import datetime
import time

import logger

from src.model.enum import Onmyoji, Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService

image_service = ImageService()
airtest_service = AirtestService()

# 共享的中断标志
project_interrupt_flag = False
# 战斗结果
fight_result = None


class TempComplexService1:
    @staticmethod
    def fight_end(fight_win: str, fight_fail: str, fight_again: str, fight_quit: str, fight_none: str = None,
                  timeouts: int = 60, timeout: int = 1):
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
        cvstrategy = Cvstrategy.sift
        rgb = False
        threshold = 0.7
        if fight_win in [Onmyoji.border_GRJJ, Onmyoji.region_LJJ]:
            cvstrategy = Cvstrategy.default
        time_start = time.time()
        while time.time() - time_start < timeouts:
            is_first = image_service.exists(fight_win, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                            threshold=threshold, wait=timeout)
            if is_first:
                image_service.exists(fight_win, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb, threshold=threshold,
                                     is_click=True, wait=timeout)
                image_service.exists(fight_quit, timeouts=timeout, is_click=True, wait=timeout)
                return fight_win
            is_second = image_service.exists(fight_quit, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                             threshold=threshold, wait=timeout)
            if is_second:
                image_service.exists(fight_quit, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb, threshold=threshold,
                                     is_click=True, wait=timeout)
                return fight_quit
            if time.time() - time_start > 1 / 2 * timeouts:
                is_third = image_service.exists(fight_again, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                                threshold=threshold, wait=timeout)
                if is_third:
                    image_service.exists(fight_fail, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                         threshold=threshold,
                                         is_click=True, wait=timeout)
                    return fight_fail
                is_fourth = image_service.exists(fight_none, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                                 threshold=threshold, wait=timeout)
                if is_fourth:
                    return fight_none


if __name__ == '__main__':
    image_service.auto_setup("1")
    now = datetime.datetime.now()
    ImageService.touch(Onmyoji.deed_TC)
    TempComplexService1.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                  Onmyoji.border_ZCTZ, Onmyoji.border_TCTZ, Onmyoji.border_GRJJ,
                                  300, 1)
    now1 = datetime.datetime.now()
    print(now1 - now)
