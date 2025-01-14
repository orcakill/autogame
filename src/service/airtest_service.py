"""
# @Time: 2023年06月13日19:24
# @Author: orcakill
# @File: airtest_service.py
# @Description: airtest接口
"""
import logging
import random
import subprocess

import cv2
import imageio
import numpy as np
import psutil
from airtest import aircv
from airtest.aircv import cv2_2_pil
from airtest.core.android import Android
from airtest.core.android.cap_methods.screen_proxy import ScreenProxy
from airtest.core.api import *
from airtest.core.helper import G
from airtest.core.settings import Settings
from exceptiongroup import catch

from src.utils.my_logger import my_logger as logger
from src.utils.utils_mail import UtilsMail
from src.utils.utils_path import UtilsPath
from src.utils.utils_time import UtilsTime

# 控制airtest的日志输出0
log_airtest = logging.getLogger("airtest")
log_airtest.setLevel(logging.CRITICAL)

# 图片点击识别等待时间(秒）·
WAIT = 0
# 图像识别阈值
THRESHOLD = 0.7
# 按住时间
DURATION = 0.1


class AirtestService:
    @staticmethod
    def auto_setup(connect_name: str):
        devices = "Android://127.0.0.1:5037/" + connect_name
        auto_setup(__file__, logdir=False, devices=[devices])

    @staticmethod
    def auto_setup_windows(hwnd: str = None, title: str = None):
        devices = "Windows:///"
        if hwnd is not None:
            devices = devices + hwnd
        elif title is not None:
            devices = devices + '?title_re=' + title + '.*'
        auto_setup(__file__, logdir=False, devices=[devices])

    @staticmethod
    def get_cap_method(serialno):
        dev = Android(serialno=serialno)
        try:
            screen_proxy = ScreenProxy.auto_setup(dev.adb, rotation_watcher=dev.rotation_watcher)
            all_methods = screen_proxy.SCREEN_METHODS
            methods_class = screen_proxy.screen_method
            for index, (key, value) in enumerate(all_methods.items(), start=1):
                if isinstance(methods_class, value):
                    logger.debug(key)
                    return key
        except Exception as e:
            logger.exception("获取截图方法异常:{}", e)
        return None

    @staticmethod
    def check_method(serialno):
        dev = Android(serialno=serialno)
        best_method = None
        try:
            screen_proxy = ScreenProxy.auto_setup(dev.adb, rotation_watcher=dev.rotation_watcher)
            all_methods = screen_proxy.SCREEN_METHODS
            # 从self.SCREEN_METHODS中，逆序取出可用的方法
            best_time = None
            for name, screen_class in reversed(all_methods.items()):
                screen = screen_class(dev.adb, rotation_watcher=dev.rotation_watcher)
                now1 = time.time()
                result = screen_proxy.check_frame(screen)
                now2 = time.time()
                best_time1 = now2 - now1
                if result:
                    if best_time1:
                        if best_time is None:
                            best_time = best_time1
                            best_method = name
                        elif best_time1 < best_time:
                            best_time = best_time1
                            best_method = name
                logger.debug("{}:{}:{}", name, result, UtilsTime.convert_seconds(best_time1))
            if best_time:
                if best_time > 10:
                    UtilsMail.send_email("阴阳师脚本", "图像单次识别超10秒", serialno + best_time)
            logger.debug("最快的截图方法{}", best_method)
            # 获取当前进程的 pid
            pid = psutil.Process(os.getpid())
            # 获取 CPU 占用百分比
            cpu_percent = pid.cpu_percent(interval=1)
            # 获取内存占用百分比
            memory_percent = pid.memory_percent()
            logger.debug("CPU占用百分比：{}%", cpu_percent)
            logger.debug("内存占用百分比：{}%", memory_percent)
        except Exception as e:
            logger.exception("获取截图方法异常:{}", e)
        return best_method

    @staticmethod
    def snapshot(name: str = None, print_image: bool = False):
        """
        这个函数是用来实时截图的。它调用了G.DEVICE的snapshot()方法来获取截图，并将结果以数组的形式返回。
        :return: 数组
        """
        screen = None
        try:
            if print_image:
                img_path = UtilsPath.get_print_image_path(name)
                screen = snapshot(img_path, quality=99)
            else:
                screen = G.DEVICE.snapshot(quality=99)
                # img_path = UtilsPath.get_print_image_path(name)
                # aircv.imwrite(img_path, screen, 99, 1200)
        except Exception as e:
            logger.debug("截图异常:{}", e)
        return screen

    @staticmethod
    def draw_rectangle(screen, x1, y1, x2, y2):
        """
        画图，根据指定范围的坐标在原图上画框
        :param screen:
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        cv2.rectangle(screen, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # 保存图片到本地磁盘
        img_path = UtilsPath.get_print_image_path()
        imageio.imsave(img_path, screen)

    @staticmethod
    def draw_point(screen, x, y, name: str = "识别截图"):
        """
        画图，根据指定范围的坐标在原图上画框
        :param name:
        :param screen:
        :param x:
        :param y:
        :return:
        """
        if screen == '':
            screen = AirtestService.snapshot(name=name)
        rgb_image = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        cv2.circle(rgb_image, (x, y), 5, (255, 0, 0), -1)
        # 保存图片到本地磁盘
        img_path = UtilsPath.get_print_image_path()
        imageio.imsave(img_path, rgb_image)

    @staticmethod
    def exists(template: Template, cvstrategy: [], timeout: float, is_throw: bool):
        """
        判断图片是否存在并返回坐标
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT_TMP = timeout
        try:
            try:
                pos = AirtestService.loop_find(template, timeout=ST.FIND_TIMEOUT_TMP, random_area=0.5)
            except TargetNotFoundError:
                return False
            else:
                return pos
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def loop_find(template: Template, timeout=ST.FIND_TIMEOUT, threshold=None, interval=0.5, intervalfunc=None,
                  random_area=0.0):
        """
        判断模板图片在设备上是否存在，如果存在返回坐标

        :param template: 图片类
        :param timeout:  超时时间
        :param threshold: 相似度
        :param interval:  识别间隔
        :param intervalfunc:
        :param random_area: 随机区域，默认0，取中心点，大于零小于等于1则区域内随机
        :return:
        """
        G.LOGGING.info("Try finding: %s", template)
        start_time = time.time()
        while True:
            screen = G.DEVICE.snapshot(filename=None, quality=ST.SNAPSHOT_QUALITY)

            if screen is None:
                G.LOGGING.warning("Screen is None, may be locked")
            else:
                if threshold:
                    template.threshold = threshold
                if 0 < random_area <= 1:
                    # 获取区域信息
                    match_rectangle = template._cv_match(screen).get("rectangle")
                    # 区域坐标
                    x1, y1 = match_rectangle[0]
                    x2, y2 = match_rectangle[1]
                    x3, y3 = match_rectangle[2]
                    x4, y4 = match_rectangle[3]
                    # 计算长方形的宽度和高度
                    width = max(x1, x2, x3, x4) - min(x1, x2, x3, x4)
                    height = max(y1, y2, y3, y4) - min(y1, y2, y3, y4)
                    # 处理随机区域
                    if random_area < 1:
                        x1, y1 = x1 + random_area * width / 2, y1 + random_area * height / 2
                        x2, y2 = x2 + random_area * width / 2, y2 - random_area * height / 2
                        x3, y3 = x3 - random_area * width / 2, y3 - random_area * height / 2
                        x4, y4 = x4 - random_area * width / 2, y4 + random_area * height / 2
                    random_x = int(random.uniform(min(x1, x2, x3, x4), max(x1, x2, x3, x4)))
                    random_y = int(random.uniform(min(y1, y2, y3, y4), max(y1, y2, y3, y4)))
                    match_pos = (random_x, random_y)
                else:
                    # 其他情况，取中心点
                    match_pos = template.match_in(screen)
                if match_pos:
                    try_log_screen(screen)
                    return match_pos

            if intervalfunc is not None:
                intervalfunc()

            # 超时则raise，未超时则进行下次循环:
            if (time.time() - start_time) > timeout:
                try_log_screen(screen)
                raise TargetNotFoundError('Picture %s not found in screen' % template)
            else:
                time.sleep(interval)

    @staticmethod
    def touch(folder_path: str, template: Template, cvstrategy: [], timeout: float, is_throw: bool, click_times: int,
              duration: float):
        """
        判断图片是否存在并返回坐标
        :param folder_path:
        :param click_times:
        :param duration:
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT_TMP = timeout
        try:
            if touch(template, times=click_times, duration=duration):
                logger.debug("图像识别点击成功{}", folder_path)
                return True
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def touch_coordinate(v: [], duration: float = DURATION, wait_time: float = WAIT):
        """
        点击坐标
        :param duration: 按住时间
        :param v: 坐标
        :param wait_time: 等待开始时间
        :return:
        """
        time.sleep(wait_time)
        if touch(v, duration=duration):
            logger.debug("坐标点击成功")
            return True
        else:
            return False

    @staticmethod
    def adb_stop_app(package: str):
        """
        停止APP
        :param package: app的包名
        :return: 无
        """
        stop_app(package=package)

    @staticmethod
    def adb_start_app(package: str):
        """
        停止APP
        :param package: app的包名
        :return: 无
        """
        start_app(package=package)

    @staticmethod
    def adb_restart_app(package: str):
        """
        重启APP
        :param package: app的包名
        :return: 无
        """
        AirtestService.adb_stop_app(package)
        time.sleep(2)
        AirtestService.adb_start_app(package)
        time.sleep(2)

    @staticmethod
    def swipe(v1: [], v2: [], duration):
        """
        滑动
        :param duration: 间隔
        :param v1: 坐标1
        :param v2: 坐标2
        :return:
        """
        if swipe(v1, v2, duration=duration):
            return True
        else:
            return False

    @staticmethod
    def crop_image(x1, y1, x2, y2):
        """
        局部截图
        :param x1: x1
        :param y1: y1
        :param x2: x2
        :param y2: y2
        :return:
        """
        screen = G.DEVICE.snapshot()
        # 局部截图
        local_screen = aircv.crop_image(screen, (x1, y1, x2, y2))
        return local_screen

    @staticmethod
    def resolution_ratio():
        """
        获取分辨率
        :return:
        """
        if G.DEVICE.display_info['orientation'] in [1, 3]:
            height = G.DEVICE.display_info['width']
            width = G.DEVICE.display_info['height']
        else:
            height = G.DEVICE.display_info['height']
            width = G.DEVICE.display_info['width']
        return width, height

    @staticmethod
    def cv2_2_pil(local):
        return cv2_2_pil(local)

    @staticmethod
    def find_all(template: Template, cvstrategy: [], timeout: float, is_throw: bool):
        """
        多图查找
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return:
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT = timeout
        try:
            result = find_all(template)
            return result
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def cv_match(template: Template, screen, cvstrategy: []):
        Settings.CVSTRATEGY = cvstrategy
        return template._cv_match(screen)

    @staticmethod
    def match_in(template: Template, screen, cvstrategy: [], timeout: float, is_throw: bool):
        """
        判断图片是否存在并返回坐标
        :param screen:   局部截图
        :param template: 图片类
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param is_throw: 是否显示异常
        :return: bool
        """
        Settings.CVSTRATEGY = cvstrategy
        Settings.FIND_TIMEOUT_TMP = timeout
        try:
            return template.match_in(screen)
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

    @staticmethod
    def text(word: str):
        """
        文字
        :param word: 文字内容
        :return:
        """
        text1 = "input text '" + word + "'"
        shell(text1)

    @staticmethod
    def get_template_list(folder_path: str, rgb: bool = False, threshold: float = THRESHOLD):
        """
        根据文件夹名获取图片集合，转为template列表
        :param threshold: 图像识别阈值
        :param rgb: RGB
        :param folder_path: 图片文件夹路径
        :return:
        """
        template_list = []
        folder_all_path = os.path.join(UtilsPath.get_onmyoji_image_path(), folder_path)
        folder_list = os.listdir(folder_all_path)
        random.shuffle(folder_list)
        for file_name in folder_list:
            file_path = os.path.abspath(os.path.join(folder_all_path, file_name))
            # 判断文件是否存在
            if os.path.isfile(file_path):
                # 判断文件是否是图片类型
                file_ext = file_path.split('.')[-1].lower()
                if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                    # 图片类赋值
                    template = Template(filename=file_path, rgb=rgb, threshold=threshold)
                    template_list.append(template)
            else:
                logger.debug("{}文件不存在", file_path)
        return template_list

    @staticmethod
    def get_adb_resolution(device_address):
        command = 'adb -s ' + device_address + ' shell wm size'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        resolution_tuple = output.decode().strip().split(' ')[-1]
        resolution_tuple = tuple(map(int, resolution_tuple.split('x')))
        if resolution_tuple:
            return resolution_tuple

    @staticmethod
    def get_color_format(arr):
        r_mean = np.mean(arr[:, :, 0])
        g_mean = np.mean(arr[:, :, 1])
        b_mean = np.mean(arr[:, :, 2])

        if r_mean > g_mean and r_mean > b_mean:
            return 'RGB'
        elif b_mean > r_mean and b_mean > g_mean:
            return 'BGR'
        else:
            # 可能需要更复杂的判断逻辑或者无法确定
            return False
