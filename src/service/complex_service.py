# @Time: 2023年08月04日 18:27
# @Author: orcakill
# @File: complex_service.py
# @Description: 复杂逻辑处理
import time

from src.model.enum import Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

image_service = ImageService()
airtest_service = AirtestService()


class ComplexService:
    @staticmethod
    def fight_end(fight_win: str, fight_fail: str, fight_again: str, fight_quit: str,fight_none:str,timeout: int):
        """
        结界战斗，结束战斗
        1、战斗胜利,退出挑战
        2、退出挑战
        3、再次挑战（只识别不点击），战斗失败
        :param fight_none: 已有挑战，什么都不做
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
                image_service.wait(fight_quit, timeout=1, is_click=True, interval=2)
                return True
            is_fail = image_service.wait(fight_again, timeout=1)
            if is_fail:
                logger.debug("战斗失败")
                image_service.wait(fight_fail, timeout=1, is_click=True, interval=2)
                return False
            is_none = image_service.wait(fight_none, timeout=1)
            if is_none:
                logger.debug("未正常退出，已有下一次挑战")
                return False
        return None

    @staticmethod
    def swipe_floor(floor: str, target: str, swipe: int, times: int):
        """
        判断是否有待选层号,有则直接选中，无则通过向
        :param floor:
        :param target:
        :param swipe:
        :param times:
        :return:
        """
        is_target = image_service.exists(target, is_click=True)
        if not is_target:
            logger.debug("无目标层号")
            # 获取层字的横坐标，向下滑动3次
            layer_coordinates = image_service.exists(floor, cvstrategy=Cvstrategy.default)
            if layer_coordinates:
                if swipe == 0:
                    xy1 = (layer_coordinates[0], layer_coordinates[1])
                    xy2 = (layer_coordinates[0], 1 / 4 * layer_coordinates[1])
                else:
                    xy1 = (layer_coordinates[0], 1 / 4 * layer_coordinates[1])
                    xy2 = (layer_coordinates[0], layer_coordinates[1])
                logger.debug("开始滑动")
                for i in range(times):
                    airtest_service.swipe(xy1, xy2)
                    is_target = image_service.exists(target, is_click=True)
                    if is_target:
                        break
        else:
            logger.debug("有目标层号")

    @staticmethod
    def top_addition(word: str, add_type: str, add_open: str, add_close: str, add_switch: int):
        """

        :param word:  加成文字
        :param add_type:  加成类型
        :param add_open: 打开加成
        :param add_close: 关闭加成
        :param add_switch:  加成开关
        :return:
        """

        coordinate_word = image_service.exists(word)
        if coordinate_word:
            logger.debug("点击顶部加成")
            coordinate_top = airtest_service.touch_coordinate(coordinate_word)
            logger.debug("根据类型确定纵坐标")
            coordinate_type = image_service.exists(add_type)
            if add_switch == 0:
                logger.debug("关闭加成")
                logger.debug("根据类型确定横坐标")
                coordinate_switch = image_service.exists(add_open)
                logger.debug("点击计算出的关闭坐标")
                airtest_service.touch_coordinate((coordinate_switch[0], coordinate_type[1]))
            else:
                logger.debug("打开加成")
                logger.debug("根据类型确定横坐标")
                coordinate_switch = image_service.exists(add_close)
                logger.debug("点击计算出的打开坐标")
                airtest_service.touch_coordinate((coordinate_switch[0], coordinate_type[1]))
            logger.debug("关闭顶部加成")
            airtest_service.touch_coordinate(coordinate_top)
        else:
            logger.debug("没找到顶部加成")
