import os
import sys

from loguru import logger

from src.utils.utils_path import get_project_path

logger.remove()  # 移除默认的日志记录器

BASE_DIR = get_project_path()
# 设置主日志文件,所有日志都会记录在此文件中
my_log_file_path = os.path.join(BASE_DIR, "src\\log\\my.log")


class MyLogger:
    def __init__(self, log_file_path=my_log_file_path):
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(sys.stdout, level='DEBUG',
                        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "  # 颜色>时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 线程名
                               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                               ":<cyan>{line}</cyan> | "  # 行号
                               "<level>{level}</level>: "  # 等级
                               "<level>{message}</level>",  # 日志内容
                        )
        # 输出到文件的格式,注释下面的add',则关闭日志写入
        self.logger.add(log_file_path, level='DEBUG',
                        format='{time:YYYY-MM-DD HH:mm:ss.SSS} - '  # 时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               '{module}.{function}:{line} - {level} -{message}',  # 模块名.方法名:行号
                        rotation="10 MB")

    def get_logger(self):
        return self.logger


my_logger = MyLogger().get_logger()
