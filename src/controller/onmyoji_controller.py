from src.dao.mapper_extend import MapperExtend
from src.utils.my_logger import my_logger as logger


def task(game_type: str, game_round: str, game_is_email: str) -> None:
    """
    项目组任务
    :param game_type: 项目类型
    :param game_round: 项目执行次数
    :param game_is_email:  项目是否发送邮件报告
    :return: None
    """
    logger.info("任务开始")
    # 获取项目组
    game_task = MapperExtend.select_game_task("", game_type)
    # 循环项目组
    for i in (1,)*int(game_round):
        logger.info("第{}轮", i)
        # 循环项目
        for j in range(len(game_task)):
            # 判断项目名称，根据项目名称执行不同的函数
            project_name=game_task[j]['GameProject'].project_name
            game_name=game_task[j]['GameAccount'].game_name
            if project_name=="当前状态初始化":
                logger.info("{}:{}",project_name,game_name)

