# @Time: 2023年08月04日 18:27
# @Author: orcakill
# @File: complex_service.py
# @Description: 复杂逻辑处理
import threading
import time

from src.model.enum import Cvstrategy, Onmyoji
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger

image_service = ImageService()
airtest_service = AirtestService()

# 共享的中断标志
fight_interrupt_flag = False
# 战斗识别结果
fight_result = None


class ComplexService:
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
        global fight_interrupt_flag
        global fight_result
        fight_interrupt_flag = False
        fight_result = None
        # 创建线程1，战斗胜利，退出挑战
        thread1 = threading.Thread(target=ComplexService.fight_end_thread,name="fight-11",
                                   args=(fight_win, True, fight_quit, True, timeouts, timeout))
        # 创建线程2，退出挑战,无
        thread2 = threading.Thread(target=ComplexService.fight_end_thread,name="fight-12",
                                   args=(fight_quit, True, None, True, timeouts, timeout))
        # 创建线程3，再次挑战，战斗失败
        thread3 = threading.Thread(target=ComplexService.fight_end_thread,name="fight-13",
                                   args=(fight_again, False, fight_fail, True, timeouts, timeout))
        # 创建线程4，未挑战
        thread4 = threading.Thread(target=ComplexService.fight_end_thread,name="fight-14",
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
        if fight_result in [fight_win, fight_quit]:
            return True
        elif fight_result in [fight_again]:
            return False
        else:
            return None

    @staticmethod
    def fight_end_thread(first, first_click, second, second_click, timeouts, timeout):
        global fight_interrupt_flag
        global fight_result
        time_start = time.time()
        cvstrategy = Cvstrategy.sift
        if first == Onmyoji.border_GRJJ:
            cvstrategy = Cvstrategy.default
        while time.time() - time_start < timeouts and not fight_interrupt_flag:
            is_first = image_service.exists(first, timeouts=timeout, is_click=first_click,
                                            cvstrategy=cvstrategy)
            if is_first:
                if second is not None:
                    image_service.exists(second, timeouts=timeout, is_click=second_click)
                fight_interrupt_flag = True
                fight_result = first
                logger.debug("提前结束：{}", first)
                return True
        logger.debug("识别结束：{}", first)
        return False

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
                    is_target = image_service.exists(target, is_click=True, timeouts=1, wait=1)
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
            coordinate_type = image_service.exists(add_type, timeouts=2)
            if add_switch == 0:
                logger.debug("关闭加成")
                logger.debug("根据类型确定横坐标")
                coordinate_switch = image_service.exists(add_open, timeouts=2)
            else:
                logger.debug("打开加成")
                logger.debug("根据类型确定横坐标")
                coordinate_switch = image_service.exists(add_close, timeouts=2)
            if coordinate_switch and coordinate_type:
                logger.debug("点击计算出的开关坐标")
                airtest_service.touch_coordinate((coordinate_switch[0], coordinate_type[1]), wait_time=2)
                logger.debug("退出顶部加成")
                airtest_service.touch_coordinate(coordinate_word, wait_time=2)
                return True
            else:
                logger.debug("未找到加成坐标")
                logger.debug("退出顶部加成")
                airtest_service.touch_coordinate(coordinate_word, wait_time=2)
        else:
            logger.debug("没找到顶部加成")
        return False

    @staticmethod
    def get_reward(reward: str):
        is_reward = image_service.exists(reward, wait=3)
        if is_reward:
            airtest_service.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
