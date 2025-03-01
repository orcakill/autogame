# @Time: 2023年08月04日 18:27
# @Author: orcakill
# @File: complex_service.py
# @Description: 复杂逻辑处理
import subprocess
import time

from airtest.core.android.cap_methods.screen_proxy import ScreenProxy
from tornado import concurrent

from src.model.enum import Cvstrategy, Onmyoji, WinProcessName, WinClassName
from src.service.airtest_service import AirtestService
from src.service.image_service import ImageService
from src.service.impl_cap.scrcpy_cap import ScrcpyCap
from src.service.windows_service import WindowsService
from src.utils.my_logger import logger
from src.utils.utils_path import UtilsPath


class ComplexService:

    @staticmethod
    def auto_setup(game_device: str, auto_adb: int = 0):
        """
        设备连接
         1、已启动的设备，不再重新启动，检查是否已就绪
         2、就绪检查1分钟，云手机无法就绪则重启软件，重新授权
         3、判断当前是否半黑屏

         0 云手机-001
         1 夜神模拟器
         2 平板
         3 手机
         4 云手机-002
        :param auto_adb: 是否自动进行ADB连接
        :param game_device: 设备号
        :return:
        """
        serialno = None
        connect_info = None
        WindowsService.delete_folder_file(UtilsPath.get_log_image_path(), 2)
        if game_device == "0" or game_device == 0:
            serialno = "127.0.0.1:50000"
            connect_info = serialno
            logger.debug("检查是否启动云手机-001")
            WindowsService.start_exe("YsConsole", "云帅云手机")
        if game_device == "1" or game_device == 1:
            logger.debug("检查是否启动夜神模拟器")
            WindowsService.start_exe("Nox", "夜神模拟器")
            serialno = "127.0.0.1:62001"
            connect_info = serialno
        if game_device == "2" or game_device == 2:
            logger.debug("检查是否启动荣耀平板9")
            serialno = "A2CDUN4312H00817"
            connect_info = serialno
        if game_device == "3" or game_device == 3:
            logger.debug("检查是否启动小米13")
            serialno = "8ce78c9f"
            connect_info = serialno
        if game_device == "4" or game_device == 4:
            logger.debug("检查是否启动云手机-002")
            WindowsService.start_exe("YsConsole", "云帅云手机")
            serialno = "127.0.0.1:50001"
            connect_info = serialno
        logger.debug("检查设备是否已就绪")
        is_state = WindowsService.get_device_status_by_ip(serialno)
        while is_state != "device":
            logger.debug("设备未就绪")
            if game_device in ['0', '4'] and auto_adb == 1:
                logger.debug("云手机自动登录")
                logger.debug("获取云手机句柄")
                hwnd = ImageService.find_hwnd(WinProcessName.phone_exe, WinClassName.phone_home)
                logger.debug("登录")
                ImageService.touch_windows(hwnd, Onmyoji.phone_DL)
                logger.debug("点击云手机窗口,选择设备列表和组的交点")
                ComplexService.touch_two_windows(hwnd, Onmyoji.phone_SBLB, Onmyoji.phone_Z, 1, 0, 0, 1)
                logger.debug("点击右侧更多")
                ImageService.touch_windows(hwnd, Onmyoji.phone_GD)
                logger.debug("点击ADB")
                ImageService.touch_windows(hwnd, Onmyoji.phone_TS)
                logger.debug("等待ADB窗口启动")
                time.sleep(5)
                logger.debug("点击界面上的授权")
                ImageService.touch_windows(hwnd, Onmyoji.phone_YXSQ)
            logger.debug("等待10s")
            time.sleep(10)
            logger.debug("重新检查是否已就绪")
            is_state = WindowsService.get_device_status_by_ip(serialno)
        if is_state == "device":
            logger.debug("设备已就绪")
        logger.debug("检查是否已连接")
        screen = AirtestService.snapshot()
        if screen is None:
            logger.debug("未连接设备，开始连接")
            if game_device in ['2', 2]:
                logger.debug("注册scrcpy windows截图")
                logger.debug("检查windows是否开启scrcpy")
                is_scrcpy = ImageService.get_all_hwnd_info(title=serialno)
                if is_scrcpy:
                    logger.debug("已开启scrcpy")
                else:
                    logger.debug("开启scrcpy")
                    str_f = ' -f'
                    str_device = ' -s ' + serialno
                    str_title = '  --window-title ' + serialno
                    str_border = ' --window-borderless'
                    str_control = ' --no-control'
                    str_size = ' --max-fps 30'
                    str_bt = " -b 8M"
                    str_audio = " --no-audio"
                    str_buffer = " --display-buffer=10"
                    str_cmd = 'scrcpy' + str_device + str_f + str_audio + str_control + str_border + str_title + str_size + str_bt + str_buffer
                    logger.debug("执行命令{}", str_cmd)
                    subprocess.Popen(str_cmd, shell=True, start_new_session=True)  # 打开scrcpy
                    time.sleep(5)
                logger.debug("注册scrcpy截图")
                ScreenProxy.register_method("SCRCPYCAP", ScrcpyCap)
                logger.debug("连接设备")
                AirtestService.auto_setup(serialno)
            else:
                logger.debug("连接设备")
                AirtestService.auto_setup(connect_info)
            logger.debug("检查截图方法")
            best_method = AirtestService.check_method(serialno)
            logger.debug("以最快截图方法重新连接")
            connect_info = connect_info + '?cap_method=' + best_method
            AirtestService.auto_setup(connect_info)
        else:
            logger.debug("已连接设备")
            logger.debug("检查截图方法")
            AirtestService.check_method(serialno)

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
        is_target = ImageService.exists(target, is_click=True, threshold=0.8)
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
        加成 开关
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
        is_reward = ImageService.exists(Onmyoji.comm_FH_XSFYHSCH, timeouts=timeouts, is_click=True, rgb=True)
        if is_reward:
            logger.debug("拒接悬赏")
        is_chat = ImageService.exists(Onmyoji.comm_LTJM, timeouts=timeouts)
        if is_chat:
            logger.debug("退出聊天")
            ImageService.touch_coordinate((3 / 2 * is_chat[0], 3 / 2 * is_chat[1]))
        return True

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
    def touch_two(folder1: str, folder2: str, rgb1: bool = True, rgb2: bool = True):
        coordinate1 = ImageService.exists(folder1, rgb=rgb1)
        coordinate2 = ImageService.exists(folder2, rgb=rgb2)
        if coordinate1 and coordinate2:
            ImageService.touch_coordinate((coordinate1[0], coordinate2[1]))
        elif not coordinate1 and not coordinate2:
            logger.debug("未找到{}和{}", folder1, folder2)
        elif not coordinate1:
            logger.debug("未找到{}", folder1)
        elif not coordinate2:
            logger.debug("未找到{}", folder2)

    @staticmethod
    def touch_two_windows(hwnd, folder1: str, folder2: str, x1: int = 1, y1: int = 1, x2: int = 0, y2: int = 0):
        coordinate1 = ImageService.exists_windows(hwnd, folder1)
        coordinate2 = ImageService.exists_windows(hwnd, folder2)
        if coordinate1 and coordinate2:
            logger.debug("图片都识别成功")
            ImageService.touch_coordinate(
                (coordinate1[0] * x1 + coordinate2[0] * x2, coordinate1[1] * y1 + coordinate2[1] * y2))
        elif not coordinate1 and not coordinate2:
            logger.debug("未找到{}和{}", folder1, folder2)
        elif not coordinate1:
            logger.debug("未找到{}", folder1)
        elif not coordinate2:
            logger.debug("未找到{}", folder2)

    @staticmethod
    def check_list(image_list: [], rgb: bool = False):
        def check_image(num, image):
            logger.debug("{} {}", num, image)
            is_num = ImageService.exists(image, rgb=rgb)
            if is_num:
                return num
            return 100

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_image, i, image_list[i]) for i in range(len(image_list))]
        results = [future.result() for future in futures]
        min_value = min(results)
        if min_value != 100:
            return image_list[min_value]
        return None
