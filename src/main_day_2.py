# @Time: 2023年09月02日 10:26
# @Author: orcakill
# @File: main_day.py
# @Description: 每日任务
import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.controller.onmyoji_controller import OnmyojiController
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    # 云手机002
    game_device = "4"
    # 0-5,6-11,12-16,17-23
    task_list1, task_list2, task_list3, task_list4 = [], [], [], []
    # 初始化项目组进度
    for i in range(10):
        task_list1.append(False)
        task_list2.append(False)
        task_list3.append(False)
        task_list4.append(False)
    # 小号
    game_id_small = '2,3,4,5'
    logger.info("云手机002,开始")
    # 获取当前日期
    today = datetime.date.today()
    start_hour, end_hour = 0, 6
    while True:
        # 获取当前时间
        current_time1 = datetime.datetime.now()
        # 获取当前时间的小时数
        current_hour = current_time1.hour
        # 获取当前时间的分钟
        current_minute = current_time1.minute
        # 获取本日是周几（周一为0，周日为6）
        weekday = today.weekday() + 1
        logger.debug("当前日期{}:{}", today, current_hour)
        if current_hour % 2 == 0 and 0 <= current_minute <= 20:
            if weekday == 3 and 6 <= current_hour <= 8:
                logger.info("周三维护中")
            else:
                start_hour, end_hour = 0, 23
                OnmyojiController.run_log("小号脚本")
                logger.info("0-23,小号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, game_id_small, project_name="式神寄养",
                                                       start_hour=start_hour, end_hour=end_hour)
        else:
            logger.info("不满足偶数点前20分钟的条件")
        # 如果当前时间大于等于0点并且小于8点
        if 0 <= current_hour <= 5:
            start_hour, end_hour = 0, 5
            if not task_list1[1]:
                logger.info("0-5,小号，好友协战")
                OnmyojiController.create_execute_tasks(game_device, game_id_small, project_name="好友协战",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list1[1] = True
                continue
            if not task_list4[2]:
                logger.info("0-5,小号，全流程任务")
                OnmyojiController.create_execute_tasks(game_device, game_id_small, projects_num="2",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[2] = True
                continue
        # 如果当前时间大于等于6点并且小于等于11点
        elif 5 <= current_hour <= 11:
            start_hour, end_hour = 5, 11
            if (weekday == 3 and current_hour >= 9) or (weekday != 3):
                if not task_list2[1]:
                    logger.info("6-11,小号，好友协战")
                    OnmyojiController.create_execute_tasks(game_device, game_id_small, project_name="好友协战",
                                                           start_hour=start_hour, end_hour=end_hour)
                    task_list1[1] = True
                    continue
        # 如果当前时间大于等于12点,小于等于16点
        elif 12 <= current_hour <= 16:
            start_hour, end_hour = 12, 17
            if not task_list3[1]:
                logger.info("12-16,小号，斗技")
                OnmyojiController.create_execute_tasks(game_device, game_id_small, project_name='斗技',
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list3[1] = True
                continue
            if not task_list3[2]:
                logger.info("12-16,小号，好友协战")
                OnmyojiController.create_execute_tasks(game_device, game_id_small, project_name="好友协战",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list1[1] = True
                continue
        # 如果当前时间大于等于17点,小于等于23点
        elif 17 <= current_hour <= 23:
            start_hour, end_hour = 17, 23
            if current_hour <= 22 and not task_list4[1]:
                logger.info("17-24,小号，逢魔之时")
                OnmyojiController.create_execute_tasks(game_device, game_id_small, project_name="逢魔之时",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[1] = True
                continue
            if 19 <= current_hour <= 20 and weekday in [5, 6, 7] and not task_list4[2]:
                logger.info("17-24,小号，阴界之门")
                OnmyojiController.create_execute_tasks(game_device, game_id_small, project_name="阴界之门",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[2] = True
                continue
            if 19 <= current_hour <= 21 and not task_list4[3]:
                logger.info("17-24,小号，全流程")
                OnmyojiController.create_execute_tasks(game_device, game_id_small, projects_num="2",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[3] = True
                continue
        # 等待5分钟
        logger.debug("等待5分钟")
        # 重新获取当前日期
        today1 = datetime.date.today()
        logger.debug("云手机002,日期对比 {}:{}", today, today1)
        if today != today1:
            today = today1
            logger.info("云手机002,已过一天，重置变量")
            for i in range(10):
                task_list1[i] = False
                task_list2[i] = False
                task_list3[i] = False
                task_list4[i] = False
