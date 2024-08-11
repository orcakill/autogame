# @Time: 2024年08月01日 08:38
# @Author: orcakill
# @File: day_1.py
# @Description: 每日任务

import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dao.mapper import Mapper
from src.dao.mapper_extend import MapperExtend
from src.model.models import GameJobLog, GameJob
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
        game_job_log_list1 = MapperExtend.select_game_job_log_all(game_job_device_id=game_device,
                                                                  game_job_day=today_str)
        game_job_log_list2 = []
        if len(game_job_log_list1) == 0:
            logger.debug("创建当日作业")
            game_job_list = MapperExtend.select_game_job_all(device_id=game_device)
            for i in game_job_list:
                game_job = GameJob(game_job_list[i])
                game_job_log = GameJobLog()
                game_job_log.job_date = today
                game_job_log.job_id = game_job.id
                game_job_log.job_state = 0
                Mapper.save_game_job_log(game_job_log)
            logger.debug("重新获取当日作业")
            game_job_log_list2 = MapperExtend.select_game_job_log_all(game_job_device_id=game_device,
                                                                      game_job_day=today_str)
        game_job_log_list = game_job_log_list1 + game_job_log_list2
        if game_job_log_list:
            logger.debug("当前作业列表")
            for game_job_log in game_job_log_list:
                logger.debug(game_job_log)
        break
