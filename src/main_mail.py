# @Time: 2024年05月30日 17:56
# @Author: orcakill
# @File: main_mail.py
# @Description: 每日邮件
import datetime
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.dao.mapper_extend import MapperExtend
from src.utils import utils_mail
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    while True:
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 获取当前时间的小时数
        current_hour = current_time.hour
        logger.debug("当前{}", current_time)
        if current_hour in [8, 14]:
            logger.debug("运行检查")
            # time.sleep(60 * 10)
            # 获取大号脚本最后一次的日期
            run_date1 = MapperExtend.select_game_run_log("大号脚本")
            run_date2 = MapperExtend.select_game_run_log("小号脚本")
            # 获取当前时间和脚本运行记录的差，如果大于6小时则发送邮件
            if run_date1:
                date1_hour = run_date1.hour
                if current_hour - date1_hour >= 8:
                    logger.debug("大号脚本运行异常，发送邮件")
                    utils_mail.send_email("大号脚本运行情况", "运行异常", "未运行")
                else:
                    logger.debug("大号脚本正常运行")
            if run_date2:
                date2_hour = run_date2.hour
                if current_hour - date2_hour >= 8:
                    logger.debug("小号脚本运行异常，发送邮件")
                    utils_mail.send_email("小号脚本运行情况", "运行异常", "未运行")
                else:
                    logger.debug("小号脚本正常运行")
        logger.debug("等待1小时")
        time.sleep(60 * 60)
