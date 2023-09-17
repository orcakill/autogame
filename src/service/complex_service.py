# @Time: 2023年08月04日 18:27
# @Author: orcakill
# @File: complex_service.py
# @Description: 复杂逻辑处理
import time

from src.model.enum import Cvstrategy, Onmyoji
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.utils.my_logger import logger


class ComplexService:

    @staticmethod
    def fight_end(fight_win: str, fight_fail: str, fight_again: str, fight_quit: str, fight_fight: str = None,
                  fight_attack: str = None, timeouts: int = 60, timeout: int = 1):
        """
        结界战斗，结束战斗
        1、战斗胜利,退出挑战
        2、退出挑战
        3、再次挑战（只识别不点击），战斗失败
        4、挑战（只识别不点击）
        :param fight_attack: 进攻
        :param timeouts: 识别最大时间
        :param fight_fight: 挑战（挑战）
        :param timeout: 超时时间
        :param fight_win: 战斗胜利
        :param fight_fail: 战斗失败
        :param fight_again:  再次挑战
        :param fight_quit:  退出挑战
        :return:
        """

        # 识别算法
        cvstrategy = Cvstrategy.sift
        rgb = False
        threshold = 0.7
        if fight_win in [Onmyoji.border_GRJJ, Onmyoji.region_LJJ]:
            cvstrategy = Cvstrategy.default
        time_start = time.time()
        while time.time() - time_start < timeouts:
            logger.debug("{}:{}", time.time() - time_start, timeouts)
            is_first = ImageService.exists(fight_win, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                           threshold=threshold, wait=timeout)
            if is_first:
                ImageService.touch_coordinate(is_first)
                ImageService.exists(fight_quit, timeouts=timeout, is_click=True, wait=timeout)
                return fight_win
            is_second = ImageService.exists(fight_quit, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                            threshold=threshold, wait=timeout)
            if is_second:
                ImageService.exists(fight_quit, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb, threshold=threshold,
                                    is_click=True, wait=timeout)
                return fight_quit
            if time.time() - time_start > 1 / 2 * timeouts or time.time() - time_start > 30:
                ComplexService.refuse_reward()
                is_third = ImageService.exists(fight_again, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                               threshold=threshold, wait=timeout)
                if is_third:
                    ImageService.exists(fight_fail, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                        threshold=threshold,
                                        is_click=True, wait=timeout)
                    return fight_fail
                is_fourth = ImageService.exists(fight_fight, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                                threshold=threshold, wait=timeout)
                if is_fourth:
                    return fight_fight
                if fight_attack:
                    is_fifth = ImageService.exists(fight_attack, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                                   threshold=threshold, wait=timeout)
                    if is_fifth:
                        return fight_attack
        return None

    @staticmethod
    def fight_end_win(fight_win: str, fight_quit: str, timeouts: int = 60, timeout: int = 1):
        """
        结界战斗，结束战斗
        1、战斗胜利,退出挑战
        2、退出挑战
        :param timeouts: 识别最大时间
        :param timeout: 超时时间
        :param fight_win: 战斗胜利
        :param fight_quit:  退出挑战
        :return:
        """
        # 识别算法
        cvstrategy = Cvstrategy.sift
        rgb = False
        threshold = 0.7
        time_start = time.time()
        while time.time() - time_start < timeouts:
            logger.debug("{}:{}", time.time() - time_start, timeouts)
            is_first = ImageService.exists(fight_win, timeouts=timeout, cvstrategy=cvstrategy, rgb=rgb,
                                           threshold=threshold, wait=timeout)
            if is_first:
                logger.debug("战斗胜利")
                ImageService.touch_coordinate(is_first)
                ImageService.exists(fight_quit, timeouts=timeout, is_click=True, wait=timeout)
                return fight_win
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
        is_target = ImageService.exists(target, is_click=True)
        xy1, xy2 = (), ()
        if not is_target:
            logger.debug("无目标{}", target)
            # 获取基础图片的坐标
            layer_coordinates = ImageService.exists(basis, cvstrategy=Cvstrategy.default)
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
                    AirtestService.swipe(xy1, xy2)
                    logger.debug("判断是否有{}", target)
                    is_target = ImageService.touch(target, wait=1)
                    if is_target:
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
        try:
            coordinate_word = ImageService.exists(word)
            if coordinate_word:
                logger.debug("点击顶部加成")
                AirtestService.touch_coordinate(coordinate_word)
                logger.debug("根据类型确定纵坐标")
                coordinate_type = ImageService.exists(add_type, timeouts=2)
                if add_switch == 0:
                    logger.debug("关闭加成")
                    logger.debug("获取加成开的个数")
                    coordinate_result = ImageService.find_all(add_open)
                    logger.debug("有{}个加成开", len(coordinate_result))
                    if len(coordinate_result) > 0:
                        logger.debug("关闭所有加成", len(coordinate_result))
                        for i in range(len(coordinate_result)):
                            ImageService.touch_coordinate(coordinate_result[i]['result'])
                    logger.debug("退出顶部加成")
                    AirtestService.touch_coordinate(coordinate_word, wait_time=2)
                else:
                    logger.debug("打开加成")
                    logger.debug("根据类型确定横坐标")
                    coordinate_switch = ImageService.exists(add_close, timeouts=2, cvstrategy=Cvstrategy.default)
                    if coordinate_switch and coordinate_type:
                        logger.debug("点击计算出的开关坐标")
                        AirtestService.touch_coordinate((coordinate_switch[0], coordinate_type[1]), wait_time=2)
                        logger.debug("退出顶部加成")
                        AirtestService.touch_coordinate(coordinate_word, wait_time=2)
                        return True
                    else:
                        logger.debug("未找到加成坐标")
                        logger.debug("退出顶部加成")
                        AirtestService.touch_coordinate(coordinate_word, wait_time=2)

            else:
                logger.debug("没找到顶部加成")
            return False
        except Exception as e:
            logger.debug("异常；{}", e)

    @staticmethod
    def get_reward(reward: str):
        is_reward = ImageService.exists(reward, wait=3)
        if is_reward:
            AirtestService.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
            return True
        return False

    @staticmethod
    def refuse_reward():
        """
        拒接悬赏
        :return:
        """
        is_reward = ImageService.touch(Onmyoji.comm_FH_XSFYHSCH, cvstrategy=Cvstrategy.default)
        if is_reward:
            logger.debug("拒接悬赏")
            return True
        return False
