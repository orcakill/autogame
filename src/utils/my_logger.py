import os
import sys

from loguru import logger

from src.utils.utils_path import UtilsPath

logger.remove()  # 移除默认的日志记录器
# 设置主日志文件目录,所有日志都会记录在此文件夹中
my_log_file_path = UtilsPath.get_project_path_log()


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

        # 信息日志配置（添加进程标识）
        self.logger.add(
            os.path.join(log_file_path, f"info/{{time:YYYY-MM-DD}}/{{time:HH-mm-ss}}_p{os.getpid()}.log"),
            level='INFO',
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} - process:{process} | thread:{thread} | {module}.{function}:{line} - {level} - {message}',
            retention="48h",
            enqueue=True,
            rotation="500 MB"
        )

        # 新增错误日志单独存储
        self.logger.add(
            os.path.join(log_file_path, f"error/{{time:YYYY-MM-DD}}/{{time:HH-mm-ss}}_p{os.getpid()}.log"),
            level='ERROR',
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} - process:{process} | thread:{thread} | {module}.{function}:{line} - {level} - {message}',
            retention="7 days",
            enqueue=True
        )

    def get_logger(self):
        return self.logger


# 屏蔽第三方包日志
logger.disable("airtest")

# 创建MyLogger实例
my_logger = MyLogger().get_logger()
