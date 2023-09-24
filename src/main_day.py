# @Time: 2023年09月02日 10:26
# @Author: orcakill
# @File: main_day.py
# @Description: 每日任务
import datetime
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.controller.onmyoji_controller import OnmyojiController
from src.dao.mapper_extend import MapperExtend
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    # 只有一台云手机，已登录账号不进行登录，无最近一小时日志记录的置为未登录，本地测试时强制更新为未登录后进行登录
    # 0点-6点  1.大号、小号 全流程任务 2大号肝绘卷
    # 6点-12点 1.大号、小号 式神寄养、地域鬼王  2。大号阴阳寮突破（肝绘卷时暂停）
    # 12点-17点 1.大号斗技式神寄养、+寮突破（肝绘卷时暂停） 2、小号斗技
    # 17点-19点 1.小号逢魔之时、大小号式神寄养
    # 默认云手机
    game_device = "1"
    volume = False
    # 式神寄养 0点
    projects1 = False
    # 小号全流程
    projects2 = False
    # 大号绘卷
    projects3 = False
    # 式神寄养  6点
    projects4 = False
    # 地域鬼王  6点或9点
    projects5 = False
    # 式神寄养  12点
    projects6 = False
    # 逢魔之时  17点
    projects7 = False
    # 式神寄养  18点
    projects8 = False
    # 小号个人突破  22点
    projects9 = False
    logger.debug("开始")
    while True:
        # 获取当前时间
        current_time1 = datetime.datetime.now()
        # 获取当前时间的小时数
        current_hour = current_time1.hour
        # 如果当前时间大于等于0点并且小于8点
        if 0 <= current_hour < 6:
            if not projects1:
                logger.debug("大号小号式神寄养，0点")
                # 获取任务
                game_tasks = OnmyojiController.create_tasks(list(['1', '2', '3', '4', '5']), "", "式神寄养")
                # 执行任务
                OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                projects1 = True
            if not projects2 and not volume:
                logger.debug("项目2，小号全流程，执行一次")
                # 获取任务
                game_tasks = MapperExtend.select_game_task("", "2")
                # 执行任务
                OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                projects2 = True
            if not projects3 and volume:
                logger.debug("项目4，大号绘卷，执行20次")
                # 获取任务
                game_tasks = MapperExtend.select_game_task("", "4")
                # 执行任务
                OnmyojiController.execute_tasks(game_tasks, "20", "1", game_device)
                projects3 = True
        # 如果当前时间大于等于6点并且小于12点
        elif 6 <= current_hour < 12:
            # 获取当前日期
            today = datetime.date.today()
            # 获取本日是周几（周一为0，周日为6）
            weekday = today.weekday() + 1
            if (weekday == 3 and current_hour >= 9) or (weekday != 3):
                if not projects4 and current_hour < 9:
                    logger.debug("大号小号式神寄养，6点")
                    # 获取任务
                    game_tasks = OnmyojiController.create_tasks(list(['1', '2', '3', '4', '5']), "", "式神寄养")
                    # 执行任务
                    OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                    projects4 = True
                if not projects5:
                    logger.debug("大号小号地域鬼王")
                    # 获取任务
                    game_tasks = OnmyojiController.create_tasks(list(['1', '2', '3', '4', '5']), "", "地域鬼王")
                    # 执行任务
                    OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                if volume:
                    logger.debug("开绘卷，大号阴阳寮挑战+个人突破+探索")
                    # 获取任务
                    game_tasks = MapperExtend.select_game_task("", "4")
                    # 执行任务
                    OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                else:
                    logger.debug("不开绘卷，大号阴阳寮挑战循环")
                    # 获取任务
                    game_tasks = MapperExtend.select_game_task("", "3")
                    # 执行任务
                    OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
        # 如果当前时间大于等于12点,小于17点
        elif 12 <= current_hour < 17:
            if not projects6:
                logger.debug("大号小号式神寄养，12点")
                # 获取任务
                game_tasks = OnmyojiController.create_tasks(list(['1', '2', '3', '4', '5']), "", "式神寄养")
                # 执行任务
                OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                projects6 = True
            logger.debug("大号阴阳寮挑战+大号小号斗技5次，循环")
            # 获取任务
            game_tasks = OnmyojiController.create_tasks(list(['1']), "", "阴阳寮突破")
            # 执行任务
            OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
            # 获取任务
            game_tasks = OnmyojiController.create_tasks(list(['1', '2', '3', '4', '5']), "", "斗技", 5)
            # 执行任务
            OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
        # 如果当前时间大于等于17点,小于23点
        elif 17 <= current_hour <= 23:
            if not projects7:
                logger.debug("小号逢魔之时")
                # 获取任务
                game_tasks = OnmyojiController.create_tasks(list(['2', '3', '4', '5']), "", "逢魔之时")
                # 执行任务
                OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                projects7 = True
            if current_hour >= 18:
                if not projects8:
                    logger.debug("大号小号式神寄养，18点")
                    # 获取任务
                    game_tasks = OnmyojiController.create_tasks(list(['1', '2', '3', '4', '5']), "", "式神寄养")
                    # 执行任务
                    OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                    projects8 = True
            if not projects9:
                logger.debug("小号个人突破+每日奖励")
                # 获取任务
                game_tasks = OnmyojiController.create_tasks(list(['2', '3', '4', '5']), "", "个人突破")
                # 执行任务
                OnmyojiController.execute_tasks(game_tasks, "1", "1", game_device)
                projects9 = True
        # 等待1分钟
        time.sleep(60)
        # 获取当前时间
        current_time2 = datetime.datetime.now()
        current_different = current_time2 - current_time1
        if current_different.days > 1:
            logger.debug("已过一天，重置变量")
            volume = False
            # 式神寄养 0点
            projects1 = False
            # 小号全流程
            projects2 = False
            # 大号绘卷
            projects3 = False
            # 式神寄养  6点
            projects4 = False
            # 地域鬼王  6点或9点
            projects5 = False
            # 式神寄养  12点
            projects6 = False
            # 逢魔之时  17点
            projects7 = False
            # 式神寄养  18点
            projects8 = False
            # 小号个人突破  22点
            projects9 = False
