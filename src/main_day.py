# @Time: 2023年09月02日 10:26
# @Author: orcakill
# @File: main_day.py
# @Description: 每日任务
import datetime
import time
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    # 只有一台云手机，已登录账号不进行登录，无最近一小时日志记录的置为未登录，本地测试时强制更新为未登录后进行登录
    # 0点-6点  1.大号、小号 全流程任务 2大号肝绘卷
    # 6点-12点 1.大号、小号 式神寄养、地域鬼王  2。大号阴阳寮突破（肝绘卷时暂停）
    # 12点-17点 1.大号斗技式神寄养、+寮突破（肝绘卷时暂停） 2、小号斗技
    # 17点-19点 1.小号逢魔之时、大小号式神寄养
    logger.debug("开始")
    while True:
        # 获取当前时间
        current_time = datetime.datetime.now()

        # 获取当前时间的小时数
        current_hour = current_time.hour

        # 如果当前时间大于等于0点并且小于8点
        if 0 <= current_hour < 6:
            logger.debug("项目1，大号全流程，执行一次")
            logger.debug("项目2，小号全流程，执行一次")
            logger.debug("如果开绘卷，大号打探索，每轮打完判断时间，在0点到6点之间")
            logger.debug("不开绘卷，休息")
        # 如果当前时间大于等于6点并且小于12点
        elif 8 <= current_hour < 12:
            logger.debug("判断当前是否周三，周三6-9点维护")
            logger.debug("大号式神寄养+地域鬼王")
            logger.debug("小号式神寄养+地域鬼王")
            logger.debug("不开绘卷，大号阴阳寮挑战循环")
            logger.debug("开绘卷，大号阴阳寮挑战+个人突破+探索")
        # 如果当前时间大于等于12点,小于17点
        elif 12 <= current_hour < 17:
            logger.debug("大号式神寄养")
            logger.debug("小号式神寄养")
            logger.debug("大号阴阳寮挑战+斗技循环")
            logger.debug("小号斗技循环")
        # 如果当前时间大于等于17点,小于20点
        elif 17 <= current_hour < 20:
            logger.debug("大号式神寄养")
            logger.debug("小号式神寄养")
            logger.debug("小号逢魔之时")
        # 等待1分钟
        time.sleep(60)
