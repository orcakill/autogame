from src.dao.mapper_extend import MapperExtend
from src.model.models import *
from src.service.onmyoji_service import OnmyojiService
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
    for i in range(int(game_round)):
        logger.info("第{}轮", i + 1)
        # 循环项目
        for j in range(len(game_task)):
            # 判断项目名称，根据项目名称执行不同的函数
            game_projects_relation = GameProjectsRelation(game_task[j][1])
            game_account = GameAccount (game_task[j][2])
            game_project = GameProject(game_task[j][3])
            logger.info("{},{}:{}", game_projects_relation.relation_num, game_project.project_name,
                        game_account.game_name)
            logger.info("当前状态初始化")
            OnmyojiService.initialization(game_account)
            if game_project.project_name in ["登录"]:
                OnmyojiService.initialization(game_account)
            elif game_project.project_name in ["魂一", "魂十", "魂十一"]:
                OnmyojiService.soul_fight(game_task[j])
        if game_is_email:
            logger.info("发送邮件")
