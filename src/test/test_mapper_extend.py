from src.dao.mapper_extend import MapperExtend
from src.utils.my_logger import my_logger as logger


def test_select_game_threads():
    # 查询测试
    game_thread1 = MapperExtend.select_game_thread("")
    logger.info(game_thread1)


def test_select_task():
    # 查询测试
    task = MapperExtend.select_game_task("", "")
    logger.info(task)
