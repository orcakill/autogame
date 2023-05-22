from src.controller.onmyoji_controller import task
from utils.my_logger import my_logger as logger
from airtest.core.api import *

if __name__ == '__main__':
    logger.info("脚本启动")
    logger.info()
    game_type = input("请输入一个脚本类型：")
    game_round = input("请输入一个脚本轮次：")
    logger.info("脚本类型 {},脚本轮次 {}", game_type, game_round)
    # 执行项目组
    # 发送邮件报告


    # 连接设备
    auto_setup(__file__, logdir=True, devices=["android://"])
    #
    # 在auto_setup接口传入devices参数
    start_app("com.netease.onmyoji")
