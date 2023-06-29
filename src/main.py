import os

from src.controller.onmyoji_controller import task
from src.service.airtest_service import AirtestService
from utils.my_logger import my_logger as logger

# 导入 airtest服务接口
airtest_service = AirtestService()

if __name__ == '__main__':
    logger.info("脚本启动")
    logger.info("1 大号、小号、协战号每日任务")
    logger.info("2 协战号寄养、协战、领取奖励")
    logger.info("0  默认设备 1 夜神模拟器")
    game_type = input("请输入一个脚本类型：")
    game_round = input("请输入一个脚本轮次：")
    game_device=input("请输入一个脚本设备：")
    # 0 每个节点都发送邮件 1 进程结束后发送邮件  2不发送邮件
    game_is_email = "0"
    logger.info("脚本类型 {},脚本轮次 {}", game_type, game_round)
    logger.info("连接Android设备")
    # 连接android设备
    airtest_service.auto_setup(game_device)
    # 执行项目组、每个节点整理邮件报告
    task(game_type, game_round, game_is_email)
