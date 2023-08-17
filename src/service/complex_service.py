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
    def fight_end(fight_win: str, fight_fail: str, fight_again: str, fight_quit: str, fight_none: str, timeout: int):
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
    def swipe_floor(basis: str, target: str, swipe: int, times: int):
        """
        判断是否有待选层号,有则直接选中，无则通过向
        :param basis: 基础图片
        :param target: 目标图片
        :param swipe:  滑动方向 0 向上滑动 1 向下滑动 2 向左滑动 3 向右滑动
        :param times:  滑动次数
        :return:
        """
        is_target = image_service.exists(target, is_click=True)
        xy1, xy2 = (), ()
        if not is_target:
            logger.debug("无目标{}", target)
            # 获取基础图片的坐标
            layer_coordinates = image_service.exists(basis, cvstrategy=Cvstrategy.default)
            if layer_coordinates:
                if swipe == 0:
                    xy1 = (layer_coordinates[0], 1 / 4 * layer_coordinates[1])
                    xy2 = (layer_coordinates[0], layer_coordinates[1])
                elif swipe == 1:
                    xy1 = (layer_coordinates[0], layer_coordinates[1])
                    xy2 = (layer_coordinates[0], 1 / 4 * layer_coordinates[1])
                elif swipe == 2:
                    xy1 = (layer_coordinates[0], layer_coordinates[1])
                    xy2 = (1 / 4 * layer_coordinates[0], layer_coordinates[1])
                elif swipe == 3:
                    xy1 = (1 / 4 * layer_coordinates[0], layer_coordinates[1])
                    xy2 = (layer_coordinates[0], layer_coordinates[1])
                logger.debug("开始滑动")
                for i in range(times):
                    logger.debug("滑动{}次", i + 1)
                    airtest_service.swipe(xy1, xy2)
                    is_target = image_service.exists(target, is_click=True, timeouts=1, interval=1)
                    if is_target:
                        logger.debug("发现目标{}", target)
                        break
        else:
            logger.debug("发现目标{}", target)

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
            airtest_service.touch_coordinate(coordinate_word)
            logger.debug("根据类型确定纵坐标")
            coordinate_type = image_service.exists(add_type, timeouts=1)
            if add_switch == 0:
                logger.debug("关闭加成")
                logger.debug("根据类型确定横坐标")
                coordinate_switch = image_service.exists(add_open, timeouts=1)
            else:
                logger.debug("打开加成")
                logger.debug("根据类型确定横坐标")
                coordinate_switch = image_service.exists(add_close, timeouts=1)
            if coordinate_switch and coordinate_type:
                logger.debug("点击计算出的关闭坐标")
                airtest_service.touch_coordinate((coordinate_switch[0], coordinate_type[1]))
            else:
                logger.debug("未找到加成坐标")
            logger.debug("关闭顶部加成")
            airtest_service.touch_coordinate(coordinate_word)
        else:
            logger.debug("没找到顶部加成")

    @staticmethod
    def get_reward(reward: str):
        is_reward = image_service.exists(reward, interval=3)
        if is_reward:
            airtest_service.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
