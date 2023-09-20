import random
import time

from src.dao.mapper_extend import MapperExtend
from src.model.models import *
from src.service.image_service import ImageService
from src.service.onmyoji_service import OnmyojiService
from src.utils.my_logger import my_logger as logger
from src.utils.utils_time import UtilsTime


class OnmyojiController:
    @staticmethod
    def tasks(game_type: str, game_round: str, game_is_email: str, relation_num: str, game_device: str) -> None:
        """
        项目组任务
        :param game_device: 设备序号
        :param game_type: 项目类型
        :param game_round: 项目执行次数
        :param game_is_email:  项目是否发送邮件报告
        :param relation_num:  项目中断后重新执行的序号
        :return: None
        """
        try:
            time_start = time.time()
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
                        ImageService.auto_setup(game_device)
                        is_initialization = OnmyojiService.initialization(game_task[j])
                        if is_initialization:
                            # 项目 1、24 每日奖励领取
                            if game_project.project_name in ["登录"]:
                                OnmyojiService.initialization(game_task[j])
                            # 项目 2
                            elif game_project.project_name in ["每日奖励"]:
                                OnmyojiService.daily_rewards(game_task[j])
                            # 项目 3
                            elif game_project.project_name in ["逢魔之时"]:
                                OnmyojiService.encounter_demons(game_task[j])
                            # 项目 4
                            elif game_project.project_name in ["地域鬼王"]:
                                OnmyojiService.ghost_king(game_task[j])
                            # 项目 5
                            elif game_project.project_name in ["式神寄养"]:
                                OnmyojiService.foster_care(game_task[j])
                            # 项目 5
                            elif game_project.project_name in ["阴阳寮管理"]:
                                OnmyojiService.shack_house(game_task[j])
                            # 项目 7
                            elif game_project.project_name in ["阴阳寮突破"]:
                                OnmyojiService.region_border(game_task[j])
                                if game_projects_relation.wait_after_time and game_projects_relation.wait_after_time > 0:
                                    time_time = game_projects_relation.wait_after_time
                                    logger.debug("战斗结束后等待一段时间")
                                    result_time = random.randint(time_time - 5, time_time + 5)
                                    logger.debug("等待{}分钟", result_time)
                                    time.sleep(result_time * 60)
                            # 项目 8
                            elif game_project.project_name in ["个人突破"]:
                                OnmyojiService.border_fight(game_task[j])
                            # 项目 9
                            elif game_project.project_name in ["好友管理"]:
                                OnmyojiService.friends_manage(game_task[j])
                            # 项目 10
                            elif game_project.project_name in ["好友协战"]:
                                OnmyojiService.friends_fight(game_task[j])
                            # 项目 11
                            elif game_project.project_name in ["觉醒十"]:
                                OnmyojiService.awakening(game_task[j])
                            # 项目 12,13,14,15
                            elif game_project.project_name in ["魂一", "魂十", "魂十一", "魂十二"]:
                                OnmyojiService.soul_fight(game_task[j])
                            # 项目 16
                            elif game_project.project_name in ["业原火"]:
                                OnmyojiService.soul_fight_fire(game_task[j])
                            # 项目 17
                            elif game_project.project_name in ["日轮之陨"]:
                                OnmyojiService.soul_fight_sun(game_task[j])
                            # 项目 18
                            elif game_project.project_name in ["永生之海"]:
                                OnmyojiService.soul_fight_sea(game_task[j], 1)
                            # 项目 19
                            elif game_project.project_name in ["斗技"]:
                                OnmyojiService.pvp(game_task[j])
                            # 项目 21
                            elif game_project.project_name in ["探索"]:
                                OnmyojiService.explore_chapters(game_task[j])
                        else:
                            logger.debug("当前状态初始化失败{}，不执行项目", game_account.game_name)
                        time_end = time.time()
                        logger.info("{}:{},项目组累计执行时间{}", game_account.game_name, game_project.project_name,
                                    UtilsTime.convert_seconds(time_end - time_start))
                if game_is_email:
                    logger.info("发送邮件")
        except Exception as e:
            logger.exception(e)
