from src.dao.mapper_extend import MapperExtend
from src.utils.my_logger import my_logger as logger


def task(game_type: str, game_round: str, game_is_email: str):
    logger.info("任务开始")
    # 获取项目组
    game_task = MapperExtend.select_game_task("", game_type)
    # 循环项目组
    for i in (1, game_round):
        logger.info("第{}轮", i)
