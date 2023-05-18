from src.utils.my_logger import my_logger as logger
from src.model.param import *
from src.model.enum import *


def task(game_type: int, game_round: int):
    project_list = []
    if game_type == 1:
        logger.info("大号：寄养+地域鬼王+组队挑战+阴阳寮突破+结界突破+御魂40次+好友增删+花合战奖励")
        logger.info("协战号1、2、3：寄养+地域鬼王+组队挑战+结界突破协战2次+御魂协战14次+好友增删+花合战奖励")
        logger.info("大号体验服：寄养+地域鬼王+组队挑战+阴阳寮突破+结界突破+御魂40次+好友增删+花合战奖励")
        logger.info("小号1：寄养+地域鬼王+组队挑战+阴阳寮突破+结界突破+御魂40次+好友增删+花合战奖励")
        project_list.append(ProjectParam(ProjectEnum.project_JYJC,))
    projects = ProjectsParam(ProjectsEnum.project_1.value, game_round, [])
    return projects
