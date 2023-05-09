from src.python.utils.my_logger import MyLogger

from airtest.core.api import *
import configparser
from pathlib import Path

if __name__ == '__main__':
    log = MyLogger().get_logger()
    log.info("脚本启动")

    config = configparser.ConfigParser()
    project_path = Path.cwd().parent
    config_path = Path(project_path.joinpath("resources"), "config.ini")
    config.read(config_path,encoding="utf-8")
    log.info(config.get("DATABASE", "url"))
    # 在auto_setup接口传入devices参数
    # auto_setup(__file__, logdir=True, devices=["android://"])
    # start_app("com.netease.onmyoji")
