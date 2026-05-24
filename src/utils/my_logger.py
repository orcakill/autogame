import os
import sys
from loguru import logger
from src.utils.utils_path import UtilsPath

my_log_file_path = UtilsPath.get_project_path_log()

class MyLogger:
    def __init__(self, log_file_path=my_log_file_path):
        self.logger = logger
        self.logger.remove()  # 只在这里移除一次
        self.configure_logger(log_file_path)

    def configure_logger(self, log_file_path):
        self._ensure_log_directory(log_file_path)

        # 控制台输出（修正 process 和 thread）
        self.logger.add(
            sys.stdout,
            level='DEBUG',
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "{process} | "
                "{thread} | "
                "<cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{level}</level>: <level>{message}</level>"
            )
        )

        # INFO 日志文件
        self.logger.add(
            os.path.join(log_file_path, f"info/{{time:YYYY-MM-DD}}/{{time:HH-mm-ss}}_p{os.getpid()}.log"),
            level='INFO',
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} - process:{process} | thread:{thread} | {module}.{function}:{line} - {level} - {message}',
            retention="48h",
            enqueue=True,
            rotation="500 MB"
        )

        # DEBUG 日志文件
        self.logger.add(
            os.path.join(log_file_path, f"debug/{{time:YYYY-MM-DD}}/{{time:HH-mm-ss}}_p{os.getpid()}.log"),
            level='DEBUG',
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} - process:{process} | thread:{thread} | {module}.{function}:{line} - {level} - {message}',
            retention="48h",
            enqueue=True,
            rotation="500 MB"
        )

        # ERROR 日志文件
        self.logger.add(
            os.path.join(log_file_path, f"error/{{time:YYYY-MM-DD}}/{{time:HH-mm-ss}}_p{os.getpid()}.log"),
            level='ERROR',
            format='{time:YYYY-MM-DD HH:mm:ss.SSS} - process:{process} | thread:{thread} | {module}.{function}:{line} - {level} - {message}',
            retention="7 days",
            enqueue=True
        )

    @staticmethod
    def _ensure_log_directory(log_file_path):
        sub_dirs = ['info', 'debug', 'error', 'bat', 'image']
        for sub_dir in sub_dirs:
            dir_path = os.path.join(log_file_path, sub_dir)
            os.makedirs(dir_path, exist_ok=True)

    def get_logger(self):
        return self.logger

# 屏蔽 airtest 的 logging 日志（如果是 logging 模块）
import logging
logging.getLogger("airtest").setLevel(logging.WARNING)

# 创建单例 logger
my_logger = MyLogger().get_logger()

if __name__ == '__main__':
    logger.debug("测试")