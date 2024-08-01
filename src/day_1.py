# @Time: 2024年08月01日 08:38
# @Author: orcakill
# @File: day_1.py
# @Description: 每日任务

import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.controller.onmyoji_controller import OnmyojiController
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    # 云手机001
    game_device = "822aeaf9-47f5-11ef-ac7d-fa163e9ff72f"
    while True:
        # 获取当前日期
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        # 获取当前时间
        current_time1 = datetime.datetime.now()
        # 获取当前时间的小时数
        current_hour = current_time1.hour
        # 获取当前时间的分钟
        current_minute = current_time1.minute
        # 获取本日是周几（周一为0，周日为6）
        weekday = today.weekday() + 1
        # 获取当日作业记录，无当日作业记录则插入作业记录
