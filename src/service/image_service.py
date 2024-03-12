# @Time    : 2023年06月16日 09:15
# @Author  : orcakill
# @File    : image_service.py
# @Description : 图像识别接口
import os
import random
import time

from airtest.core.cv import Template

from src.model.enum import Cvstrategy
from src.service.airtest_service import AirtestService
from src.service.windows_service import WindowsService
from src.utils.my_logger import my_logger as logger
from src.utils.utils_path import get_onmyoji_image_path

# 图像识别算法
CVSTRATEGY = Cvstrategy.sift
# 单张图片识别时间
TIMEOUT = 0.5
# 图片组识别时间
TIMEOUTS = 5
# 图像识别阈值
THRESHOLD = 0.7
# 图片识别轮次
REC_ROUND = 1
# 图片等待识别时间(秒）·
WAIT = 2
# 图片识别间隔(秒）·
INTERVAL = 1
# 点击次数
TIMES = 1
# 按住时间
DURATION = 0.01

THROW = False


class ImageService:
    @staticmethod
    def exists(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: float = TIMEOUTS,
               threshold: float = THRESHOLD, wait: float = WAIT, interval: float = INTERVAL, is_throw: bool = THROW,
               is_click: bool = False, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在

        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :param interval: 图片识别点击间隔时间
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_click: 是否点击坐标
        :param is_throw: 是否显示异常
        :return:
        """
        try:
            time.sleep(wait)
            template_list = ImageService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    pos = AirtestService.exists(template, cvstrategy, timeout, is_throw)
                    if pos and not is_click:
                        if is_throw:
                            logger.debug("图像识别成功:{},{}", folder_path, template.filename)
                        else:
                            logger.debug("图像识别成功:{}", folder_path)
                        return pos
                    if pos and is_click:
                        time.sleep(interval)
                        logger.debug("图像识别点击成功:{}", folder_path)
                        ImageService.touch_coordinate(pos)
                        return True
            return False
        except Exception as e:
            if is_throw:
                logger.exception("异常：{}", e)
            else:
                pass
        return False

    @staticmethod
    def touch(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: float = TIMEOUTS,
              threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW, times: int = TIMES,
              duration: float = DURATION, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，点击图片
        :param rgb: rgb
        :param timeouts: 图片组超时时间
        :param wait: 点击间隔时间
        :param times: 点击次数
        :param duration: 按住时间
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 超时时间
        :param threshold: 图像识别阈值
        :param is_throw: 是否显示异常,默认不显示异常
        :return: bool
        """
        try:
            time.sleep(wait)
            template_list = ImageService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    is_click = AirtestService.touch(template, cvstrategy, timeout, is_throw, times, duration)
                    if is_click:
                        # word=folder_path.replace("\\","_")
                        # ImageService.snapshot(word, True)
                        logger.debug("图像识别点击成功:{}", folder_path)
                        return True
            return False
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass

        return False

    @staticmethod
    def auto_setup(game_device: str):
        """
                设备连接
                1、已启动的设备，不再重新启动，检查是否已就绪
                2、就绪检查1分钟，云手机无法就绪则重启软件，重新授权
                3、判断当前是否半黑屏
                :return:
                """
        devices_name = None
        connect_name = None
        if game_device == "0":
            logger.debug("检查是否启动云手机-001")
            WindowsService.start_exe("YsConsole", "云帅云手机")
            devices_name = "127.0.0.1:50000"
            connect_name = devices_name
        if game_device == "1":
            logger.debug("检查是否启动夜神模拟器")
            WindowsService.start_exe("Nox", "夜神模拟器")
            devices_name = "127.0.0.1:62001"
            connect_name = devices_name + "?cap_method=JAVACAP"
        if game_device == "2":
            logger.debug("检查是否启动荣耀平板5")
            devices_name = "E8X9X19719000371"
            connect_name = devices_name
        if game_device == "3":
            logger.debug("检查是否启动小米13")
            devices_name = "8ce78c9f"
            connect_name = devices_name
        if game_device == "4":
            logger.debug("检查是否启动云手机-002")
            WindowsService.start_exe("YsConsole", "云帅云手机")
            devices_name = "127.0.0.1:50001"
            connect_name = devices_name + "?cap_method=JAVACAP"
        logger.debug("判断设备是否已就绪")
        is_state = WindowsService.get_device_status_by_ip(devices_name)
        while is_state != "device":
            logger.debug("未就绪，设备状态{},等待10s", is_state)
            time.sleep(10)
            logger.debug("重新判断是否已就绪")
            is_state = WindowsService.get_device_status_by_ip(devices_name)
        if is_state == "device":
            logger.debug("设备已就绪")
        logger.debug("连接设备")
        AirtestService.auto_setup(connect_name)

    @staticmethod
    def snapshot(name: str = None, print_image: bool = False):
        """
        设备截图
        :return:
        """
        return AirtestService.snapshot(name, print_image)

    @staticmethod
    def touch_coordinate(v: [], wait: float = WAIT, duration: float = DURATION):
        """
        点击坐标
        :param duration: 按住时间
        :param v: 坐标
        :param wait: 等待开始时间
        :return:
        """

        AirtestService.touch_coordinate(v, wait, duration)

    @staticmethod
    def restart_app(app: str):
        """
        重启APP
        :param app: 包名
        :return:
        """
        AirtestService.restart_app(app)

    @staticmethod
    def stop_app(app: str):
        """
        重启APP
        :param app: 包名
        :return:
        """
        AirtestService.stop_app(app)

    @staticmethod
    def swipe(v1: [], v2: [], duration: float = 0.5):
        """
        滑动
        :param duration: 间隔
        :param v1: 坐标1
        :param v2: 坐标2
        :return:
        """
        AirtestService.swipe(v1, v2, duration)

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
        return AirtestService.crop_image(x1, y1, x2, y2)

    @staticmethod
    def resolution_ratio():
        """
        获取分辨率
        :return:
        """
        return AirtestService.resolution_ratio()

    @staticmethod
    def cv2_2_pil(local):
        """
        转换图片格式
        :param local:图片
        :return:
        """
        return AirtestService.cv2_2_pil(local)

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
        folder_all_path = os.path.join(get_onmyoji_image_path(), folder_path)
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
    def find_all(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: int = TIMEOUTS,
                 threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                 rgb: bool = False):
        """
        多图查找
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            template_list = ImageService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    pos = AirtestService.find_all(template, cvstrategy, timeout, is_throw)
                    if pos:
                        logger.debug("图像查找成功:{}", folder_path)
                        return pos
            return None
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass
        return None

    @staticmethod
    def find_all_coordinate(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                            timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                            is_throw: bool = THROW, rgb: bool = False):
        """
        多图查找 只获取坐标
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            template_list = ImageService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    pos = AirtestService.find_all(template, cvstrategy, timeout, is_throw)
                    if pos:
                        logger.debug("图像查找成功:{}", folder_path)
                        return [d['result'] for d in pos]
            return None
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass
        return None

    @staticmethod
    def find_all_num(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT, timeouts: int = TIMEOUTS,
                     threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                     rgb: bool = False):
        result = ImageService.find_all(folder_path, cvstrategy, timeout, timeouts, threshold, wait, is_throw, rgb)
        if result:
            return len(result)
        else:
            return 0

    @staticmethod
    def cv_match(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeouts: int = TIMEOUTS,
                 threshold: float = THRESHOLD, wait: float = WAIT, is_throw: bool = THROW,
                 rgb: bool = False, x1: float = 0, x2: float = 1, y1: float = 0, y2: float = 1):
        """
        计算图片和设备截图的匹配结果，有result 坐标  confidence 相似度 区域范围
         :param cvstrategy: 图像识别算法
        :param y2: y2坐标比例
        :param x2: x2坐标比例
        :param y1: y1坐标比例
        :param x1: x1坐标比例
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            resolution = ImageService.resolution_ratio()
            time.sleep(wait)
            template_list = ImageService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    # 设备截图
                    image1 = ImageService.crop_image(x1 * resolution[0], y1 * resolution[1], x2 * resolution[0],
                                                     y2 * resolution[1])
                    return AirtestService.cv_match(template, image1, cvstrategy)
            return None
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass
        return None

    @staticmethod
    def crop_exists(folder_path1: str, folder_path2: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                    timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                    is_throw: bool = THROW, rgb: bool = False):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path1: 图片文件夹路径1 局部图
        :param folder_path2: 图片文件夹路径2 局部图内图片
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            result = ImageService.cv_match(folder_path1)
            if result:
                result_xy1 = result['rectangle'][0]
                result_xy2 = result['rectangle'][1]
                result_screen = ImageService.crop_image(result_xy1[0], result_xy1[1], result_xy2[0], result_xy2[1])
                template_list = ImageService.get_template_list(folder_path2, rgb, threshold)
                time_start = time.time()
                while time.time() - time_start < timeouts:
                    for template in template_list:
                        pos = AirtestService.match_in(template, result_screen, cvstrategy, timeout, is_throw)
                        if pos:
                            if is_throw:
                                logger.debug("局部图内图像识别成功:{},{}", folder_path2, template.filename)
                            else:
                                logger.debug("局部图内图像识别成功:{}", folder_path2)
                            return pos
            return False
        except Exception as e:
            if is_throw:
                logger.exception("异常：{}", e)
            else:
                pass
        return False

    @staticmethod
    def text(word: str):
        """
        文字
        :param word: 文字内容
        :return:
        """
        AirtestService.text(word)

    @staticmethod
    def touch_all_coordinate(folder_path: str, cvstrategy: [] = CVSTRATEGY, timeout: float = TIMEOUT,
                             timeouts: int = TIMEOUTS, threshold: float = THRESHOLD, wait: float = WAIT,
                             is_throw: bool = THROW, rgb: bool = False, rank: int = 1):
        """
        多图查找 只获取坐标
        :param rank: 点击第几个
        :param rgb: 带颜色
        :param timeouts: 图片组超时时间
        :param wait: 图片等待识别时间
        :param is_throw: 是否显示异常
        :param folder_path: 图片文件夹路径
        :param cvstrategy: 图像识别算法
        :param timeout: 单张图片超时时间
        :param threshold: 图像识别阈值
        :return:
        """
        try:
            time.sleep(wait)
            template_list = ImageService.get_template_list(folder_path, rgb, threshold)
            time_start = time.time()
            while time.time() - time_start < timeouts:
                for template in template_list:
                    pos = AirtestService.find_all(template, cvstrategy, timeout, is_throw)
                    if pos and len(pos) >= rank - 1:
                        coordinate = pos[rank - 1]['result']
                        logger.debug("图像查找点击成功:{},坐标{}", folder_path, coordinate)
                        ImageService.touch_coordinate(coordinate)
                        return coordinate
            return False
        except Exception as e:
            if is_throw:
                logger.error("异常：{}", e)
            else:
                pass
        return False
