import os
import sys

from loguru import logger

from src.utils.utils_path import get_project_path_log

logger.remove()  # 移除默认的日志记录器
# 设置主日志文件目录,所有日志都会记录在此文件夹中
my_log_file_path = get_project_path_log()


class MyLogger:
    def __init__(self, log_file_path=my_log_file_path):
        self.logger = logger
        self.logger.remove()
        self.configure_logger(log_file_path)

    def configure_logger(self, log_file_path):
        # 添加控制台输出的格式
        self.logger.add(
            sys.stdout,
            level='DEBUG',
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                   "{process.name} | "
                   "{thread.name} | "
                   "<cyan>{module}</cyan>.<cyan>{function}</cyan>"
                   ":<cyan>{line}</cyan> | "
                   "<level>{level}</level>: "
                   "<level>{message}</level>",
        )

        # 输出到文件的格式，按日期分割日志文件，并设置日志文件名
        self.logger.add(
            os.path.join(log_file_path, "debug/{time:YYYY-MM-DD_HH-mm-ss}.log"),
            level='DEBUG',
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} - '
                   "{process.name} | "
                   "{thread.name} | "
                   '{module}.{function}:{line} - {level} - {message}',
            retention="48h"
        )

        # 输出到文件的格式，按日期分割日志文件，并设置日志文件名
        self.logger.add(
            os.path.join(log_file_path, "info/{time:YYYY-MM-DD_HH-mm-ss}.log"),
            level='INFO',
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} - '
                   "{process.name} | "
                   "{thread.name} | "
                   '{module}.{function}:{line} - {level} - {message}',
            retention="48h"
        )

        # 输出到文件的格式，按日期分割日志文件，并设置日志文件名
        self.logger.add(
            os.path.join(log_file_path, "error/{time:YYYY-MM-DD_HH-mm-ss}.log"),
            level='ERROR',
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} - '
                   "{process.name} | "
                   "{thread.name} | "
                   '{module}.{function}:{line} - {level} - {message}',
            retention="48h"
        )

    def get_logger(self):
        return self.logger


# 屏蔽第三方包日志
logger.disable("airtest")

# 创建MyLogger实例
my_logger = MyLogger().get_logger()
