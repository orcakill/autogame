import datetime
import threading
import time

from src.model.enum import Onmyoji, Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

image_service = ImageService()
airtest_service = AirtestService()

# 共享的中断标志
project_interrupt_flag = False
# 战斗结果
fight_result = None


class TempComplexService:
    @staticmethod
    def fight_end(fight_win: str, fight_fail: str, fight_again: str, fight_quit: str, fight_none: str, timeouts: float,
                  timeout: float):
        """
        结界战斗，结束战斗
        1、战斗胜利,退出挑战
        2、退出挑战
        3、再次挑战（只识别不点击），战斗失败
        :param timeouts: 识别最大时间
        :param fight_none: 已有挑战，什么都不做
        :param timeout: 超时时间
        :param fight_win: 战斗胜利
        :param fight_fail: 战斗失败
        :param fight_again:  再次挑战
        :param fight_quit:  退出挑战
        :return:
        """
        logger.debug("创建线程1，战斗胜利，退出挑战")
        thread1 = threading.Thread(target=TempComplexService.fight_end_thread,
                                   args=(fight_win, True, fight_quit, True, timeouts, timeout))
        logger.debug("创建线程2，退出挑战,无")
        thread2 = threading.Thread(target=TempComplexService.fight_end_thread,
                                   args=(fight_quit, True, None, True, timeouts, timeout))
        logger.debug("创建线程3，再次挑战，战斗失败")
        thread3 = threading.Thread(target=TempComplexService.fight_end_thread,
                                   args=(fight_again, False, fight_fail, True, timeouts, timeout))
        logger.debug("创建线程4，未挑战")
        thread4 = threading.Thread(target=TempComplexService.fight_end_thread,
                                   args=(fight_none, False, None, True, timeouts, timeout))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        logger.debug("等待线程结束")
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        logger.debug("主函数执行完毕")
        print(fight_result)
        return fight_result

    @staticmethod
    def fight_end_thread(first, first_click, second, second_click, timeouts, timeout):
        global project_interrupt_flag
        global fight_result
        time_start = time.time()
        while time.time() - time_start < timeouts and not interrupt_flag:
            logger.debug("识别中：{}".format(first))
            is_first = image_service.exists(first, timeouts=timeout, is_click=first_click,
                                            cvstrategy=Cvstrategy.default)
            if is_first:
                if second is not None:
                    image_service.exists(second, timeouts=timeout, is_click=second_click, cvstrategy=Cvstrategy.default)
                interrupt_flag = True
                fight_result = first
                logger.debug("提前结束：{}".format(first))
                return True
        logger.debug("结束：{}".format(first))
        return False


if __name__ == '__main__':
    image_service.auto_setup("0")
    now = datetime.datetime.now()
    TempComplexService.fight_end(Onmyoji.border_ZDSL, Onmyoji.border_ZDSB,
                                 Onmyoji.border_ZCTZ, Onmyoji.border_TCTZ, Onmyoji.border_GRJJ,
                                 300, 1)
    now1 = datetime.datetime.now()
    print(now1 - now)
