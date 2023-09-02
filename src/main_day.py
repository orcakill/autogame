# @Time: 2023年09月02日 10:26
# @Author: orcakill
# @File: main_day.py
# @Description: 每日任务
import datetime
import time

from src.controller.onmyoji_controller import OnmyojiController
from src.service.image_service import ImageService
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    # 只有一台云手机，已登录账号不进行登录，无最近一小时日志记录的置为未登录，本地测试时强制更新为未登录后进行登录
    # 0点-6点  1.大号、小号 全流程任务 2大号肝绘卷
    # 6点-12点 1.大号、小号 式神寄养、地域鬼王  2。大号阴阳寮突破（肝绘卷时暂停）
    # 12点-17点 1.大号斗技式神寄养、+寮突破（肝绘卷时暂停） 2、小号斗技
    # 17点-19点 1.小号逢魔之时、大小号式神寄养
    logger.debug("开始")
    while True:
        # 获取当前时间
        current_time = datetime.datetime.now()

        # 获取当前时间的小时数
        current_hour = current_time.hour

        # 如果当前时间大于等于0点并且小于8点
        if current_hour >= 0 and current_hour < 8:
            print("1")

        # 如果当前时间大于等于8点并且小于12点
        elif current_hour >= 8 and current_hour < 12:
            print("2")

        # 如果当前时间大于等于12点
        elif current_hour >= 12:
            print("3")

        # 等待1分钟
        time.sleep(60)
