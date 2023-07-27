import logging
import logging.handlers
import sys

from loguru import logger

handler = logging.handlers.SysLogHandler(address=('localhost', 514))
logger.add(handler)


class LoguruHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[LoguruHandler()], level=0, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%Y-%M-%D %H:%M:%S')

logger.configure(handlers=[
    {
        "sink": sys.stderr,
        "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "  # 颜色>时间
                  "{process.name} | "  # 进程名
                  "{thread.name} | "  # 进程名
                  "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                  ":<cyan>{line}</cyan> | "  # 行号
                  "<level>{level}</level>: "  # 等级
                  "<level>{message}</level>",  # 日志内容
        "colorize": True
    },
])

if __name__ == '__main__':
    log = logging.getLogger('root')
    # 使用标注日志系统输出
    log.info('hello wrold, that is from logging')
    log.debug('debug hello world, that is from logging')
    log.error('error hello world, that is from logging')
    log.warning('warning hello world, that is from logging')

    # 使用loguru系统输出
    logger.info('hello world, that is from loguru')
