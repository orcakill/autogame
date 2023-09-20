# @Time: 2023年08月30日 15:20
# @Author: orcakill
# @File: main1.py
# @Description: 夜神模拟器运行
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.service.image_service import ImageService
from utils.my_logger import my_logger as logger
from src.controller.onmyoji_controller import OnmyojiController
# 导入 airtest服务接口
image_service = ImageService()

if __name__ == '__main__':
    logger.info("脚本启动")
    logger.info("**************")
    logger.info("1 大号全流程任务")
    logger.info("2 小号全流程任务")
    logger.info("3 大小号式神寄养")
    logger.info("4 大号阴阳寮突破")
    logger.info("默认夜神模拟器")
    logger.info("**************")
    # game_type = input("请输入一个脚本类型：")
    # game_round = input("请输入一个脚本轮次：")
    # game_device=input("请输入一个脚本设备：")
    game_type = "5"
    game_round = "10"
    game_device = "1"
    game_relation_num = "1"
    # 0 每个节点都发送邮件 1 进程结束后发送邮件  2不发送邮件
    game_is_email = "0"
    logger.info("**************")
    logger.info("脚本类型{},脚本轮次 {},连接设备夜神模拟器", game_type, game_round)
    logger.info("**************")
    logger.info("执行任务")
    OnmyojiController.tasks(game_type, game_round, game_is_email, game_relation_num, game_device)
