# @Time: 2023年09月02日 10:26
# @Author: orcakill
# @File: main_day.py
# @Description: 每日任务
import datetime
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dao.mapper_extend import MapperExtend
from src.service.windows_service import WindowsService
from src.controller.onmyoji_controller import OnmyojiController
from src.utils.my_logger import my_logger as logger

if __name__ == '__main__':
    WindowsService.limit_cpu_percentage(30)
    # 设备：云手机001
    game_device = "0"
    # 账号：大号、小号、大小号
    game_account_large = '1'
    game_account_small = '2,3,4,5'
    game_account_all = '1,2,3,4,5'
    logger.info("云手机001,开始")
    # 获取当前日期
    today = datetime.date.today()
    start_hour, end_hour = 0, 23
    num_round=1
    while True:
        logger.debug("第{}轮次开始",num_round)
        # 获取当前时间
        current_time1 = datetime.datetime.now()
        # 获取当前时间的小时数·
        current_hour = current_time1.hour
        # 获取当前时间的分钟
        current_minute = current_time1.minute
        # 获取本日是周几（周一为0，周日为6）
        weekday = today.weekday() + 1
        logger.debug("当前日期{}:{}:{}", today, current_hour, current_minute)
        logger.debug("检查最近3小时是否式神寄养成功")
        foster_care_records = MapperExtend.select_foster_carer(game_account_large, 3)
        if not foster_care_records:
            logger.debug("最近3小时无寄养记录")
            if weekday == 3 and 6 <= current_hour <= 8:
                logger.info("周三维护中")
            else:
                start_hour, end_hour = 0, 23
                logger.info("0-23,大小号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, game_account_all, project_name="式神寄养",
                                                       start_hour=start_hour, end_hour=end_hour)
        else:
            logger.info("最近3小时有寄养记录")
        # 如果当前时间大于等于0点并且小于23点，大号绘卷
        start_hour, end_hour = 0, 22
        logger.info("0-23,大号，大号绘卷")
        OnmyojiController.create_execute_tasks(game_device, game_account_large, projects_num="4",
                                                       start_hour=start_hour, end_hour=end_hour)
        # 等待5分钟
        logger.debug("等待5分钟")
        time.sleep(60 * 5)
        logger.debug("第{}轮次结束", num_round)
