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
from src.utils.utils_time import UtilsTime
from src.controller.onmyoji_controller import OnmyojiController
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    # 云手机001
    game_device = "0"
    # 特殊模式 ，绘卷，超鬼王
    is_mode = ""
    # 0-5
    task_list1 = []
    # 6-11
    task_list2 = []
    # 12-16
    task_list3 = []
    # 17-23
    task_list4 = []
    # 初始化项目组进度
    for i in range(10):
        task_list1.append(False)
        task_list2.append(False)
        task_list3.append(False)
        task_list4.append(False)
    # 大号
    game_id_large = '1'
    logger.info("云手机001,开始")
    # 获取当前日期
    today = datetime.date.today()
    start_hour, end_hour = 0, 6
    while True:
        # 获取当前时间
        current_time1 = datetime.datetime.now()
        # 获取当前时间的小时数
        current_hour = current_time1.hour
        # 获取本日是周几（周一为0，周日为6）
        weekday = today.weekday() + 1
        logger.debug("当前日期{}:{}", today, current_hour)
        # 如果当前时间大于等于0点并且小于8点
        if 0 <= current_hour <= 5:
            # 0点-5点 大号-式神寄养，签到，每日奖励，阴阳寮管理，好友管理，御魂20次，每日奖励，御魂整理
            #             周一，每日奖励额外检查每周奖励及神龛
            #             周一、六、日，日轮之陨50次
            #             周二、三、四，业原火20次
            #             周五，永生之海30次
            #             周一，契灵1轮
            #             周一，月之海2次
            start_hour, end_hour = 0, 5
            if not task_list1[1]:
                OnmyojiController.run_log("大号脚本")
                logger.info("0-5,大号，大号全流程任务")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, projects_num="1",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list1[1] = True
                continue
            if not task_list1[2]:
                if weekday in [1, 6, 7]:
                    logger.info("0-5,周一、六、日，大号，日轮之陨")
                    OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name="日轮之陨",
                                                           start_hour=start_hour, end_hour=end_hour)
                elif weekday in [2, 3, 4]:
                    logger.info("0-5,周二、三、四，大号，业原火")
                    project_num_times = {'业原火': 20}
                    OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name="业原火",
                                                           project_num_times=project_num_times,
                                                           start_hour=start_hour, end_hour=end_hour)
                elif weekday in [5]:
                    logger.info("0-5,周五，大号，永生之海")
                    OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name="永生之海",
                                                           start_hour=start_hour, end_hour=end_hour)
                task_list1[2] = True
                continue
            if is_mode == "绘卷":
                logger.debug("开绘卷")
                logger.info("0-5,大号，绘卷项目组")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, projects_num="4",
                                                       start_hour=start_hour, end_hour=end_hour)
        # 如果当前时间大于等于6点并且小于等于11点
        elif 5 <= current_hour <= 11:
            # 6点-12点 大号-式神寄养，地域鬼王，阴阳寮突破循环
            start_hour, end_hour = 5, 11
            if weekday == 3 and current_hour <= 7:
                logger.info("周三 5-11,大号阴阳寮突破循环")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, projects_num="3",
                                                       start_hour=start_hour, end_hour=end_hour)
            if (weekday == 3 and current_hour >= 9) or (weekday != 3):
                if is_mode == "" and not task_list2[1]:
                    OnmyojiController.run_log("大号脚本")
                    logger.info("5-11,大号,地域鬼王")
                    OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name='地域鬼王',
                                                           start_hour=start_hour, end_hour=end_hour)
                    task_list2[1] = True
                if is_mode == "" and not task_list2[2]:
                    day = UtilsTime.get_day_str()
                    region_over = MapperExtend.select_region_over(day, game_id_large)
                    if not region_over:
                        logger.debug("阴阳寮突破进度100%")
                        task_list2[2] = True
                        continue
                    logger.info("5-12,大号阴阳寮突破循环")
                    OnmyojiController.create_execute_tasks(game_device, game_id_large, projects_num="3",
                                                           start_hour=start_hour, end_hour=end_hour)
                if is_mode == "绘卷":
                    logger.debug("开绘卷")
                    logger.info("5-11,大号，绘卷项目组")
                    OnmyojiController.create_execute_tasks(game_device, game_id_large, projects_num="4",
                                                           start_hour=start_hour, end_hour=end_hour)
        # 如果当前时间大于等于12点,小于17点
        elif 12 <= current_hour <= 16:
            start_hour, end_hour = 12, 16
            if not task_list3[1]:
                OnmyojiController.run_log("大号脚本")
                logger.info("12-16,17点,大号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name="式神寄养",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list3[1] = True
                continue
            if not task_list3[2]:
                OnmyojiController.run_log("大号脚本")
                day = UtilsTime.get_day_str()
                region_over = MapperExtend.select_region_over(day, game_id_large)
                if not region_over:
                    logger.debug("阴阳寮突破进度100%")
                    task_list3[2] = True
                    continue
                logger.info("12-17,大号阴阳寮突破循环")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name="阴阳寮突破",
                                                       start_hour=start_hour, end_hour=end_hour)
            if not task_list3[3]:
                logger.info("12-16,大号，斗技")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name='斗技',
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list3[3] = True
            if is_mode == "绘卷":
                logger.debug("开绘卷")
                logger.info("12-17,大号，绘卷项目组")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, projects_num="4",
                                                       start_hour=start_hour, end_hour=end_hour)
        # 如果当前时间大于等于17点,小于24点
        elif 17 <= current_hour <= 23:
            # 17点-19点 大号-式神寄养，逢魔之时
            # 19点-23点 大号，周一到周四，狩猎战，道馆突破
            #          大号，周五到周日，狭间暗域，首领退治
            start_hour, end_hour = 17, 23
            if not task_list4[1]:
                OnmyojiController.run_log("大号脚本")
                logger.info("17-24,17点,大号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name="式神寄养",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[1] = True
                continue
            if current_hour <= 17 and not task_list4[2]:
                logger.info("17-24,17点，大号，逢魔之时")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name="逢魔之时",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[2] = True
                continue
            if current_hour == 20 and weekday in [5, 6, 7] and not task_list4[3]:
                logger.info("17-24,大号，阴界之门")
                OnmyojiController.create_execute_tasks(game_device, game_id_large, project_name="阴界之门",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[3] = True
                continue
        # 等待1分钟
        time.sleep(60 * 5)
        # 重新获取当前日期
        today1 = datetime.date.today()
        logger.debug("云手机001,日期对比 {}:{}", today, today1)
        if today != today1:
            today = today1
            logger.info("云手机001,已过一天，重置变量")
            for i in range(10):
                task_list1[i] = False
                task_list2[i] = False
                task_list3[i] = False
                task_list4[i] = False
