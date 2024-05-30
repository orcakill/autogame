# @Time: 2024年05月30日 17:56
# @Author: orcakill
# @File: main_mail.py
# @Description: 每日邮件
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    while True:
        # 获取当前时间
        current_time1 = datetime.datetime.now()
        # 获取当前时间的小时数
        current_hour = current_time1.hour
        if current_hour in [8,14]:
            # 获取大号脚本最后一次的日期
            run_date=Mapper.select_game_account()
            # 获取当前时间
