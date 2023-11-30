# @Time: 2023年08月04日 18:27
# @Author: orcakill
# @File: complex_service.py
# @Description: 复杂逻辑处理
import time

from src.model.enum import Cvstrategy, Onmyoji
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
        if fight_fight in [Onmyoji.border_GRJJ, Onmyoji.region_LJJ]:
            cvstrategy = Cvstrategy.default
        time_start = time.time()
        time.sleep(timeout)
        while time.time() - time_start < timeouts:
            logger.debug("{}:{}", round(time.time() - time_start), timeouts)
            # 1、战斗胜利+退出挑战
            logger.debug("战斗胜利")
            is_first = ImageService.touch(fight_win, timeouts=1, cvstrategy=cvstrategy, rgb=rgb, threshold=threshold,
                                          wait=0)
            if is_first:
                ImageService.touch(fight_quit, timeouts=1, wait=2)
                return fight_win
            # 2、退出挑战
            logger.debug("退出挑战")
            is_second = ImageService.exists(fight_quit, timeouts=1, cvstrategy=cvstrategy, rgb=rgb, threshold=threshold,
                                            wait=0)
            if is_second:
                ImageService.touch(fight_quit, timeouts=1, cvstrategy=cvstrategy, rgb=rgb, threshold=threshold, wait=2)
                return fight_quit
            # 3、战斗失败，未挑战
            if time.time() - time_start > 1 / 2 * timeouts or time.time() - time_start > 30:
                # 战斗失败
                logger.debug("战斗失败")
                is_third = ImageService.exists(fight_again, timeouts=1, cvstrategy=cvstrategy, rgb=rgb,
                                               threshold=threshold, wait=0)
                if is_third:
                    ImageService.touch(fight_fail, timeouts=1, cvstrategy=cvstrategy, rgb=rgb, threshold=threshold,
                                       wait=0)
                    return fight_fail
                logger.debug("未挑战")
                # 未挑战
                is_fourth = ImageService.exists(fight_fight, timeouts=1, cvstrategy=cvstrategy, rgb=rgb,
                                                threshold=threshold, wait=0)
                if is_fourth:
                    return fight_fight
                # 未进攻
                if fight_attack:
                    logger.debug("未进攻")
                    is_fifth = ImageService.exists(fight_attack, timeouts=1, cvstrategy=cvstrategy, rgb=rgb,
                                                   threshold=threshold, wait=0)
                    if is_fifth:
                        return fight_attack
                # 拒接悬赏
                logger.debug("拒接悬赏")
                ComplexService.refuse_reward(1)
            # 4、失联掉线
            if time.time() - time_start > 3 / 4 * timeouts:
                #  失联
                logger.debug("失联掉线")
                is_conn = ComplexService.loss_connection(1)
                if is_conn:
                    return is_conn
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
                    ImageService.swipe(xy1, xy2)
                    logger.debug("判断是否有{}", target)
                    is_target = ImageService.touch(target, wait=1)
                    if is_target:
                        return True
            else:
                logger.debug("无{}", basis)
                return False
        else:
            logger.debug("发现目标{}", target)
        return True

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
                ImageService.touch_coordinate(coordinate_word)
                logger.debug("根据加成类型确定纵坐标")
                coordinate_type = None
                if add_type == Onmyoji.explore_JYJC:
                    logger.debug("御魂加成向觉醒加成滑动一次")
                    coordinate_soul = ImageService.exists(Onmyoji.soul_BQ_YHJC)
                    coordinate_awaken = ImageService.exists(Onmyoji.awaken_JXJC)
                    if coordinate_soul is not None and coordinate_awaken is not None:
                        ImageService.swipe(coordinate_soul, coordinate_awaken)
                        logger.debug("{},2个坐标", add_type)
                        coordinate_type = ImageService.find_all_coordinate(add_type)
                else:
                    logger.debug("{},1个坐标", add_type)
                    coordinate_type = [ImageService.exists(add_type)]
                if coordinate_type is not None:
                    if add_switch == 1:
                        logger.debug("打开加成")
                        logger.debug("获取加成关坐标")
                        coordinate_switch = ImageService.exists(add_close, cvstrategy=Cvstrategy.default)
                        logger.debug("根据加成类型和加成关坐标计算点击加成开")
                        if coordinate_switch and coordinate_type:
                            logger.debug("点击计算出的开关坐标")
                            logger.debug(len(coordinate_type))
                            for i_click in range(len(coordinate_type)):
                                logger.debug("第{}次点击", i_click + 1)
                                coordinate_click = (coordinate_switch[0], coordinate_type[i_click][1])
                                logger.debug(coordinate_click)
                                ImageService.touch_coordinate(coordinate_click, wait=2)
                                time.sleep(1)
                            logger.debug("退出顶部加成")
                            ImageService.touch(word, wait=2)
                            return True
                        else:
                            logger.debug("未找到加成坐标")
                            logger.debug("退出顶部加成")
                            ImageService.touch(word, wait=2)
                            return False
                    else:
                        logger.debug("关闭所有的加成开")
                        for i_close in range(2):
                            logger.debug("第{}次检查", i_close + 1)
                            coordinate_result = ImageService.find_all(add_open)
                            if len(coordinate_result) > 0:
                                for i in range(len(coordinate_result)):
                                    ImageService.touch_coordinate(coordinate_result[i]['result'])
                        logger.debug("退出顶部加成")
                        ImageService.touch(word, wait=2)
                        return True
                else:
                    logger.debug("未找到加成类型坐标")
                    logger.debug("退出顶部加成")
                    ImageService.touch(word, wait=2)
                    return False
            else:
                logger.debug("没找到顶部加成")
            return False
        except Exception as e:
            logger.debug("异常；{}", e)
            logger.debug("退出顶部加成")
            ImageService.touch(word)

    @staticmethod
    def get_reward(reward: str):
        is_reward = ImageService.exists(reward, wait=3)
        if is_reward:
            ImageService.touch_coordinate((1 / 2 * is_reward[0], 1 / 2 * is_reward[1]))
            return True
        return False

    @staticmethod
    def refuse_reward(timeouts: float = 3):
        """
        拒接悬赏
        :return:
        """
        is_reward = ImageService.touch(Onmyoji.comm_FH_XSFYHSCH, cvstrategy=Cvstrategy.default, timeouts=timeouts)
        if is_reward:
            logger.debug("拒接悬赏")
            return True
        return False

    @staticmethod
    def refuse_cache(timeouts: float = 3):
        """
        清理缓存
        :return:
        """
        is_reward = ImageService.exists(Onmyoji.home_HCGD, cvstrategy=Cvstrategy.default, timeouts=timeouts)
        if is_reward:
            logger.debug("清理缓存,不再提示，确定")
            ImageService.touch(Onmyoji.home_BZTS)
            ImageService.touch(Onmyoji.home_QD)
            return True
        return False

    @staticmethod
    def loss_connection(timeouts: float = 3):
        """
        失联掉线  或 其它设备登录
        :param timeouts:
        :return:
        """
        is_connection = ImageService.touch(Onmyoji.comm_SL, cvstrategy=Cvstrategy.default, timeouts=timeouts)
        is_login = ImageService.touch(Onmyoji.comm_QTSBDL, cvstrategy=Cvstrategy.default, timeouts=timeouts)
        if is_connection or is_login:
            if is_connection:
                logger.debug("失联掉线")
            if is_login:
                logger.debug("其他设备登录")
            return Onmyoji.comm_SL
        else:
            return False

    @staticmethod
    def touch_two(folder1: str, folder2: str, num1: int, num2: int):
        coordinate1 = ImageService.find_all_coordinate(folder1)[num1 + 1]
        coordinate2 = ImageService.find_all_coordinate(folder2)[num2 + 2]
        if coordinate1 and coordinate2:
            ImageService.touch_coordinate(coordinate1[0], coordinate2[0])
        elif not coordinate1 and not coordinate2:
            logger.debug("未找到{}和{}", folder1, folder2)
        elif not coordinate1:
            logger.debug("未找到{}", folder1)
        elif not coordinate2:
            logger.debug("未找到{}", folder2)
