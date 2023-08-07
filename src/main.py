import threading

from src.controller.onmyoji_controller import task, assist
from src.service.airtest_service import AirtestService
from utils.my_logger import my_logger as logger

# 导入 airtest服务接口
airtest_service = AirtestService()

if __name__ == '__main__':
    logger.info("脚本启动")
    logger.info("**************")
    logger.info("1 大号全流程任务")
    logger.info("2 小号全流程任务")
    logger.info("0  默认设备 1 夜神模拟器")
    logger.info("**************")
    # game_type = input("请输入一个脚本类型：")
    # game_round = input("请输入一个脚本轮次：")
    # game_device=input("请输入一个脚本设备：")
    game_type = "2"
    game_round = "1"
    game_device = "0"
    # 0 每个节点都发送邮件 1 进程结束后发送邮件  2不发送邮件
    game_is_email = "0"
    logger.info("**************")
    logger.info("脚本类型{},脚本轮次 {},连接设备{}", game_type, game_round, game_device)
    logger.info("**************")
    logger.info("连接Android设备")
    # 连接android设备
    airtest_service.auto_setup(game_device)
    logger.info("创建任务线程")
    thread1 = threading.Thread(target=task, args=(game_type, game_round, game_is_email))
    thread2 = threading.Thread(target=assist,args=())
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


    # 执行项目组、每个节点整理邮件报告

#    项目：
#        当前状态初始化
#            (1) 登录（共6个账号，已完成2个）
#        单人御魂挑战
#            (1)魂一
#            (2)魂八
#            (3)魂十
#            (4)魂十一
#            (5)魂十二
#        结界突破
#            (1)退9打9
#            (2)能打则打，3次打不过直接刷新
#        阴阳寮突破
#        每日奖励
#             (1)签到
#             (2)勾玉领取
#             (3)体力领取
#             (4)御魂加成领取
#             (5)商店推荐每日一点
#         结界
#             (1)寄养检查领取
#             (2)结界卡放置、领取结界奖励
#             (3)式神育成
#         探索（任意章节、任意难度）
#         地域鬼王
#             (1)极地域鬼王
#             (2)地域鬼王
#         觉醒-水、火、风、雷（默认打雷）
#         御灵-龙、狐、豹、雀（默认打豹子）
#         契灵
#            (1)探查
#            (2)契石召唤(默认镇墓兽)
#            (3)契灵战斗
#         道馆
#         狭间暗域
#         阴界之门
#         御魂整理
#            (1)贪吃鬼，清理五星以下御魂
#            (2)五星御魂，六星不足4条副属性御魂奉纳
#            (3)六星御魂4条副属性强化
#            (4)弃置御魂处理
#         逢魔之时
#            (1)逢魔四连点
#            (2)逢魔极boss战斗
#            (3)逢魔boss战斗
#         百鬼夜行
