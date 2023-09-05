import datetime
import threading
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

image_service = ImageService()
airtest_service = AirtestService()


class TempComplexService:
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
        fight_interrupt_flag = False
        fight_result = None

        def fight_end_thread(first, first_click, second, second_click, timeouts, timeout, again: bool = False):
            nonlocal fight_interrupt_flag, fight_result
            time_start = time.time()
            cvstrategy = Cvstrategy.sift
            rgb = False
            threshold = 0.7
            if first in [Onmyoji.border_GRJJ, Onmyoji.region_LJJ]:
                cvstrategy = Cvstrategy.default
            while time.time() - time_start < timeouts and not fight_interrupt_flag:
                is_first = image_service.exists(first, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                                threshold=threshold, wait=timeout)
                if is_first and not fight_interrupt_flag:
                    fight_interrupt_flag = True
                    fight_result = first
                    logger.debug("提前结束：{}", first)
                    if first_click and again:
                        image_service.exists(first, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                             threshold=threshold, is_click=True, wait=timeout)
                    elif first_click and not again:
                        image_service.touch_coordinate(is_first)
                    if second is not None:
                        image_service.exists(second, timeouts=timeout, is_click=second_click, wait=timeout)
                    return True
            logger.debug("识别结束：{}", first)
            return False

        with ThreadPoolExecutor(max_workers=4) as executor:
            tasks = [
                executor.submit(partial(fight_end_thread, fight_win, True, fight_quit, True, timeouts, timeout, True)),
                executor.submit(partial(fight_end_thread, fight_quit, True, None, True, timeouts, timeout, False)),
                executor.submit(partial(fight_end_thread, fight_again, False, fight_fail, True, timeouts, timeout)),
                executor.submit(partial(fight_end_thread, fight_none, False, None, True, timeouts, timeout))
            ]
            for future in as_completed(tasks):
                result = future.result()
                if result:
                    break

        logger.debug("战斗结果:{}", fight_result)
        return fight_result


if __name__ == '__main__':
    image_service.auto_setup("1")
    now = datetime.datetime.now()
    ImageService.touch(Onmyoji.deed_TC)
    ComplexService.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                             Onmyoji.border_ZCTZ, Onmyoji.border_TCTZ, Onmyoji.border_GRJJ,
                             300, 1)
    now1 = datetime.datetime.now()
    print(now1 - now)
