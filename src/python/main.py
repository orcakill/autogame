from pathlib import Path

from src.python.utils.my_logger import my_logger as logger

from airtest.core.api import *

if __name__ == '__main__':
    logger.info("脚本启动")
    logger.info("1 大号+小号1+协战号123+大号体验服")
    game_type = input("请输入一个类型：")
    game_round = input("请输入一个轮次：")
    logger.info("类型 {}", game_type)
    if game_type==1:
        logger.info("大号：寄养+地域鬼王+阴阳寮突破+结界突破+御魂40次+好友增删+花合战奖励")
        logger.info("小号1：寄养+地域鬼王+阴阳寮突破+结界突破+御魂40次+好友增删+花合战奖励")
        logger.info("协战号1、2、3：寄养+地域鬼王+结界突破协战2次+御魂协战14次+好友增删+花合战奖励")
        logger.info("大号体验服：寄养+地域鬼王+阴阳寮突破+结界突破+御魂40次+好友增删+花合战奖励")
    # 在auto_setup接口传入devices参数
    auto_setup(__file__, logdir=True, devices=["android://"])
    start_app("com.netease.onmyoji")
