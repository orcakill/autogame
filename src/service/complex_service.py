# @Time: 2023年08月04日 18:27
# @Author: orcakill
# @File: complex_service.py
# @Description: 复杂逻辑处理
import time

from src.service.image_service import ImageService
from src.utils.my_logger import logger

image_service = ImageService()


class ComplexService:
    @staticmethod
    def fight_end(fight_win: str, fight_fail: str, fight_again: str, fight_quit: str, timeout: int):
        """
        结界战斗，结束战斗
        1、战斗胜利,退出挑战
        2、退出挑战
        3、再次挑战（只识别不点击），战斗失败
        :param timeout: 超时时间
        :param fight_win: 战斗胜利
        :param fight_fail: 战斗失败
        :param fight_again:  再次挑战
        :param fight_quit:  退出挑战
        :return:
        """
        time_start = time.time()
        logger.debug("判断战斗结果")
        while time.time() - time_start < timeout:
            is_quit = image_service.wait(fight_quit, timeout=1, is_click=True)
            if is_quit:
                logger.debug("直接退出挑战")
                return True
            is_win = image_service.wait(fight_win, timeout=1, is_click=True)
            if is_win:
                logger.debug("战斗胜利，退出挑战")
                image_service.wait(fight_quit, timeout=1, is_click=True,interval=2)
                return True
            is_fail = image_service.wait(fight_again, timeout=1)
            if is_fail:
                logger.debug("战斗失败")
                image_service.wait(fight_fail, timeout=1, is_click=True,interval=2)
                return False
        return None
