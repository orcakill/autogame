from src.python.utils.my_logger import logger

from airtest.core.api import *


if __name__ == '__main__':
    logger.info("脚本启动")
    # 在auto_setup接口传入devices参数
    auto_setup(__file__, logdir=True, devices=["android://"])
    start_app("com.netease.onmyoji")
