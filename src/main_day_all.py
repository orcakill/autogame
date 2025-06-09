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
from src.utils.utils_time import UtilsTime
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
    # 特殊模式处理 ，绘卷
    is_mode = ""
    # 0-5
    task_list1 = []
    # 6-11
    task_list2 = []
    # 12-16
    task_list3 = []
    # 17-23
    task_list4 = []
    # 初始化项目组任务及进度
    for i in range(10):
        task_list1.append(False)
        task_list2.append(False)
        task_list3.append(False)
        task_list4.append(False)
    logger.info("云手机001,开始")
    # 获取当前日期
    today = datetime.date.today()
    start_hour, end_hour = 0, 6
    while True:
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
            if weekday == 3 and 6 <= current_hour <= 8:
                logger.info("周三维护中")
            else:
                start_hour, end_hour = 0, 23
                logger.info("0-23,大号，式神寄养")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name="式神寄养",
                                                       start_hour=start_hour, end_hour=end_hour)
        else:
            logger.info("最近3小时有寄养记录")
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
                logger.info("0-5,小号，好友协战")
                OnmyojiController.create_execute_tasks(game_device, game_account_small, project_name="好友协战",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list1[1] = True
                continue
            if not task_list1[2]:
                logger.info("0-5,大号，大号全流程任务")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, projects_num="1",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list1[2] = True
                continue
            if not task_list1[2]:
                logger.info("0-5,大号，个人突破")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name="个人突破",
                                                       start_hour=start_hour, end_hour=end_hour)
                if weekday in [1, 6, 7]:
                    logger.info("0-5,周一、六、日，大号，日轮之陨")
                    OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name="日轮之陨",
                                                           start_hour=start_hour, end_hour=end_hour)
                elif weekday in [2, 3, 4]:
                    logger.info("0-5,周二、三、四，大号，业原火")
                    project_num_times = {'业原火': 10}
                    OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name="业原火",
                                                           project_num_times=project_num_times,
                                                           start_hour=start_hour, end_hour=end_hour)
                elif weekday in [5]:
                    logger.info("0-5,周五，大号，永生之海")
                    OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name="永生之海",
                                                           start_hour=start_hour, end_hour=end_hour)
                task_list1[2] = True
                continue
            if is_mode == "绘卷":
                logger.debug("开绘卷")
                logger.info("0-5,大号，绘卷项目组")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, projects_num="4",
                                                       start_hour=start_hour, end_hour=end_hour)
        # 如果当前时间大于等于6点并且小于等于11点
        elif 5 <= current_hour <= 11:
            # 6点-12点 大号-式神寄养，地域鬼王，阴阳寮突破循环
            start_hour, end_hour = 5, 11
            if weekday == 3 and current_hour <= 7:
                logger.info("周三 5-11,大号阴阳寮突破循环")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, projects_num="3",
                                                       start_hour=start_hour, end_hour=end_hour)
            if (weekday == 3 and current_hour >= 9) or (weekday != 3):
                if not task_list2[1]:
                    logger.info("5-11,大号,地域鬼王")
                    OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name='地域鬼王',
                                                           start_hour=start_hour, end_hour=end_hour)
                    task_list2[1] = True
                if is_mode == "" and not task_list2[2]:
                    day = UtilsTime.get_day_str()
                    region_over = MapperExtend.select_region_over(day, game_account_large)
                    if not region_over:
                        logger.debug("阴阳寮突破进度100%")
                        task_list2[2] = True
                        continue
                    logger.info("5-12,大号阴阳寮突破循环")
                    OnmyojiController.create_execute_tasks(game_device, game_account_large, projects_num="3",
                                                           start_hour=start_hour, end_hour=end_hour)
                if is_mode == "绘卷":
                    logger.debug("开绘卷")
                    logger.info("5-11,大号，绘卷项目组")
                    OnmyojiController.create_execute_tasks(game_device, game_account_large, projects_num="4",
                                                           start_hour=start_hour, end_hour=end_hour)
        # 如果当前时间大于等于12点,小于17点
        elif 12 <= current_hour <= 16:
            start_hour, end_hour = 12, 16
            day = UtilsTime.get_day_str()
            region_over = MapperExtend.select_region_over(day, game_account_large)
            if not region_over:
                logger.debug("阴阳寮突破进度100%，不再突破，改为斗技")
                task_list3[1] = True
                continue
            if not task_list3[1]:
                logger.info("12-17,大号阴阳寮突破循环")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name="阴阳寮突破",
                                                       start_hour=start_hour, end_hour=end_hour)
            if task_list3[1] and not task_list3[2]:
                logger.info("12-16,大号，斗技1")
                project_num_times = {'斗技': 5}
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name='斗技',
                                                       project_num_times=project_num_times,
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list3[2] = True
            if task_list3[1] and task_list3[3]:
                logger.info("12-16,大号，斗技2")
                project_num_times = {'斗技': 5}
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name='斗技',
                                                       project_num_times=project_num_times,
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list3[2] = True
            if is_mode == "绘卷":
                logger.debug("开绘卷")
                logger.info("12-17,大号，绘卷项目组")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, projects_num="4",
                                                       start_hour=start_hour, end_hour=end_hour)
        # 如果当前时间大于等于17点,小于20点
        elif 17 <= current_hour < 23:
            # 17点-19点 大号-  式神寄养，逢魔之时
            # 19点-23点 大号，周一到周四，狩猎战，道馆突破
            #          大号，周五到周日，狭间暗域，首领退治
            start_hour, end_hour = 17, 20
            if not task_list4[1]:
                logger.info("17-20,17点，大号，逢魔之时")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name="逢魔之时",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[1] = True
                continue
            if current_hour == 20 and weekday in [5, 6, 7] and not task_list4[2]:
                logger.info("17-20,大号，阴界之门")
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name="阴界之门",
                                                       start_hour=start_hour, end_hour=end_hour)
                task_list4[2] = True
                continue
            if not task_list3[3]:
                logger.info("17-20,大号，斗技3")
                project_num_times = {'斗技': 5}
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name='斗技',
                                                       project_num_times=project_num_times,
                                                       start_hour=start_hour, end_hour=end_hour)
            if not task_list3[4]:
                logger.info("17-20,大号，斗技4")
                project_num_times = {'斗技': 5}
                OnmyojiController.create_execute_tasks(game_device, game_account_large, project_name='斗技',
                                                       project_num_times=project_num_times,
                                                       start_hour=start_hour, end_hour=end_hour)
        elif current_hour >= 23:
            logger.debug("结束当日任务")
            sys.exit()
        # 等待5分钟
        logger.debug("等待5分钟")
        time.sleep(60 * 5)
