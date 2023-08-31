from src.controller.onmyoji_controller import OnmyojiController
from src.service.image_service import ImageService
from utils.my_logger import my_logger as logger

# 导入 airtest服务接口
image_service = ImageService()

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
    game_relation_num = "1"
    # 0 每个节点都发送邮件 1 进程结束后发送邮件  2不发送邮件
    game_is_email = "0"
    logger.info("**************")
    logger.info("脚本类型{},脚本轮次 {},连接设备{}", game_type, game_round, game_device)
    logger.info("**************")
    logger.info("连接Android设备")
    # 连接android设备
    image_service.auto_setup(game_device)
    logger.info("执行任务")
    OnmyojiController.game_thread(game_type, game_round, game_is_email, game_relation_num)

    # 执行项目组、每个节点整理邮件报告

#    项目：
#        当前状态初始化
#            (1) 登录（小号已完成）
#        每日奖励
#             (1)签到
#             (2)勾玉领取
#             (3)体力领取
#             (4)御魂觉醒加成领取
#             (5)商店推荐每日一点
#         逢魔之时
#            (1)逢魔四连点
#            (2)逢魔极boss战斗
#            (3)逢魔boss战斗
#         地域鬼王
#             (1)极地域鬼王
#             (2)地域鬼王
#         式神寄养检查
#         阴阳寮管理
#            （1）集体任务、体力、寮资金
#             (2)式神育成
#             (2)结界卡放置、领取结界奖励
#             (3)体力食盒、经验食盒
#             (4)自动合成结界卡
#        阴阳寮突破
#            (1)大号不做限制，按默认阵容随意打
#            (2)小号打一轮，无未战败的则不打，已战败则放弃
#        个人突破
#            (1)退9打9（待小号有60级再添加）
#            (2)能打则打，3次打不过直接刷新（小号已完成）
#        好友管理
#            (1)好友删除,30天不上线则删除,包括跨区
#            (2)好友添加,按推荐好友添加
#            (3)好友协战,检查当日协战次数,不足15次,则打魂十,拉协战式神出战15次
#        觉醒-水、火、风、雷（默认打雷）（小号已完成）
#        单人御魂挑战
#            (1)魂一
#            (2)魂十
#            (3)魂十一
#            (4)魂十二
#         御灵-龙、狐、豹、雀（默认打豹子）
#         契灵
#            (1)探查
#            (2)契石召唤(默认镇墓兽)
#            (3)契灵战斗
#         探索（任意章节、任意难度）
#         道馆
#         狭间暗域
#         阴界之门
#         御魂整理
#            (1)贪吃鬼，清理五星以下御魂
#            (2)五星御魂，六星不足4条副属性御魂弃置加奉纳
#            (3)六星御魂4条副属性强化
#         百鬼夜行
