import threading
import time

from src.dao.mapper_extend import MapperExtend
from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import *
from src.service.image_service import ImageService
from src.service.onmyoji_service import OnmyojiService
from src.utils.my_logger import my_logger as logger

image_service = ImageService()
project_interrupt_flag = False


class OnmyojiController:

    @staticmethod
    def game_thread(game_type: str, game_round: str, game_is_email: str, game_relation_num: str):
        thread1 = threading.Thread(target=OnmyojiController.tasks,
                                   args=(game_type, game_round, game_is_email, game_relation_num))
        thread2 = threading.Thread(target=OnmyojiController.assist, args=())
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

    @staticmethod
    def tasks(game_type: str, game_round: str, game_is_email: str, relation_num: str) -> None:
        global project_interrupt_flag
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
                game_account = GameAccount(game_task[j][2])
                game_project = GameProject(game_task[j][3])
                if game_projects_relation.relation_num >= int(relation_num):
                    logger.info("{},{}:{}", game_projects_relation.relation_num, game_project.project_name,
                                game_account.game_name)
                    logger.info("当前状态初始化")
                    is_initialization = OnmyojiService.initialization(game_task[j])
                    if is_initialization:
                        if game_project.project_name in ["登录"]:
                            OnmyojiService.initialization(game_task[j])
                        elif game_project.project_name in ["每日奖励"]:
                            OnmyojiService.daily_rewards(game_task[j])
                        elif game_project.project_name in ["逢魔之时"]:
                            OnmyojiService.encounter_demons(game_task[j])
                        elif game_project.project_name in ["地域鬼王"]:
                            OnmyojiService.ghost_king(game_task[j])
                        elif game_project.project_name in ["觉醒十"]:
                            OnmyojiService.awakening(game_task[j])
                        elif game_project.project_name in ["魂一", "魂十", "魂十一"]:
                            OnmyojiService.soul_fight(game_task[j])
                        elif game_project.project_name in ["个人突破"]:
                            OnmyojiService.border_fight(game_task[j])
                        elif game_project.project_name in ["好友管理"]:
                            OnmyojiService.friends_manage(game_task[j])
                        elif game_project.project_name in ["好友协战"]:
                            OnmyojiService.friends_fight(game_task[j])
                        elif game_project.project_name in ["式神寄养"]:
                            OnmyojiService.foster_care(game_task[j])
                    else:
                        logger.debug("当前状态初始化失败{}", game_account.game_name)
            if game_is_email:
                logger.info("发送邮件")
        project_interrupt_flag = True

    @staticmethod
    def assist():
        global project_interrupt_flag
        logger.debug("开启拒接协战")
        while not project_interrupt_flag:
            time.sleep(30)
            image_service.touch(Onmyoji.comm_FH_XSFYHSCH,cvstrategy=Cvstrategy.default)
