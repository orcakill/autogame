# @Time: 2023年09月02日 10:26
# @Author: orcakill
# @File: main_day.py
# @Description: 每日任务
import datetime
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controller.onmyoji_controller import OnmyojiController
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    # 只有一台云手机，已登录账号不进行登录，无最近一小时日志记录的置为未登录，本地测试时强制更新为未登录后进行登录
    # 0点-5点  1.大号、小号 全流程任务 2大号肝绘卷
    # 6点-12点 1.大号、小号 式神寄养、地域鬼王  2。大号阴阳寮突破（肝绘卷时暂停）
    # 12点-17点 1.大号斗技式神寄养、+寮突破（肝绘卷时暂停） 2、小号斗技
    # 17点-19点 1.小号逢魔之时、大小号式神寄养
    # 默认云手机
    game_device = "0"
    volume = False
    # 0-5
    task_list1 = []
    # 6-11
    task_list2 = []
    # 12-16
    task_list3 = []
    # 17-23
    task_list4 = []
    for i in range(1, 10):
        task_list1.append(False)
        task_list2.append(False)
        task_list3.append(False)
        task_list4.append(False)
    logger.info("开始")
    while True:
        # 获取当前时间
        current_time1 = datetime.datetime.now()
        # 获取当前时间的小时数
        current_hour = current_time1.hour
        # 获取当前日期
        today = datetime.date.today()
        # 获取本日是周几（周一为0，周日为6）
        weekday = today.weekday() + 1
        # 如果当前时间大于等于0点并且小于8点
        if 0 <= current_hour < 5:
            if not task_list1[1] and not volume:
                logger.info("0-6,小号，全流程")
                OnmyojiController.create_execute_tasks(game_device, "2", "", '0')
                task_list1[1] = True
            if not task_list1[2] and volume:
                logger.info("0-6,大号，绘卷20次")
                OnmyojiController.create_execute_tasks(game_device, "4", "", '1', game_round="20")
                task_list1[2] = True
        # 如果当前时间大于等于6点并且小于12点
        elif 5 <= current_hour < 12:
            if (weekday == 3 and current_hour >= 9) or (weekday != 3):
                if not task_list2[1]:
                    logger.info("6-12,大号，阴阳寮突破")
                    OnmyojiController.create_execute_tasks(game_device, "", "阴阳寮突破", '1')
                    logger.info("6-12,大小号，式神寄养")
                    OnmyojiController.create_execute_tasks(game_device, "", "式神寄养", '0')
                    task_list2[1] = True
                if volume:
                    logger.info("6-12,开绘卷，大号，阴阳寮挑战+个人突破+探索")
                    OnmyojiController.create_execute_tasks(game_device, "4", "", '1')
                else:
                    logger.info("6-12,不开绘卷，大号阴阳寮挑战循环")
                    OnmyojiController.create_execute_tasks(game_device, "3", "", '1')
        # 如果当前时间大于等于12点,小于17点
        elif 12 <= current_hour < 17:
            if not task_list3[1]:
                logger.info("12-17,大小号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, "", "式神寄养", '0')
            if not task_list3[2]:
                logger.info("12-17,大小号,地域鬼王")
                OnmyojiController.create_execute_tasks(game_device, "", "地域鬼王", '0')
                task_list3[1] = True
            if not task_list3[3]:
                logger.info("12-17,大小号,斗技")
                OnmyojiController.create_execute_tasks(game_device, "", "斗技", '0', project_num_times=5)
                task_list3[1] = True
            if not task_list3[4]:
                logger.info("12-17,大号小号,每日奖励")
                OnmyojiController.create_execute_tasks(game_device, "", "每日奖励", '0')
                task_list3[4] = True
            if current_hour < 17 and not task_list3[3]:
                logger.info("12-17,大号，魂十一")
                OnmyojiController.create_execute_tasks(game_device, "", "魂十一", '1', project_num_times=20)
                task_list3[3] = True
            if current_hour < 17 and not task_list3[4]:
                if weekday in [1, 6, 7]:
                    logger.info("12-17,周一、六、日，大号，日轮之陨")
                    OnmyojiController.create_execute_tasks(game_device, "", "日轮之陨", '1')
                elif weekday in [2, 3, 4]:
                    logger.info("12-17,周二、三、四，大号，业原火")
                    OnmyojiController.create_execute_tasks(game_device, "", "业原火", '1', project_num_times=20)
                elif weekday in [5]:
                    logger.info("12-17,周五，大号，永生之海")
                    OnmyojiController.create_execute_tasks(game_device, "", "永生之海", '1')
                task_list3[4] = True
            if current_hour < 17 and not task_list3[5]:
                logger.info("12-17,大号，个人突破")
                OnmyojiController.create_execute_tasks(game_device, "", "个人突破", '1')
                logger.info("12-17,大号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, "5", "", '1')
                task_list3[5] = True
        # 如果当前时间大于等于17点,小于24点
        elif 17 <= current_hour <= 23:
            if current_hour < 19 and not task_list4[1]:
                logger.info("17-24,17点,小号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, "", "式神寄养", '1')
                task_list4[1] = True
            if current_hour < 22 and not task_list4[2]:
                logger.info("17-24,小号，逢魔之时")
                OnmyojiController.create_execute_tasks(game_device, "", "逢魔之时", '2')
                task_list4[2] = True
            if current_hour >= 23 and not task_list4[3]:
                logger.info("17-24,23点,大小号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, "", "式神寄养", '0')
                task_list4[3] = True
        # 等待1分钟
        time.sleep(60)
        # 获取当前时间
        current_time2 = datetime.datetime.now()
        current_different = current_time2 - current_time1
        if current_different.days > 1:
            logger.info("已过一天，重置变量")
            volume = False
            task_list1 = []
            for i in range(1, 20):
                task_list1.append(False)
