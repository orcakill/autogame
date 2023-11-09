import datetime
import os
import random
import time

from src.dao.mapper import Mapper
from src.dao.mapper_extend import MapperExtend
from src.model.models import *
from src.service.image_service import ImageService
from src.service.onmyoji_service import OnmyojiService
from src.service.windows_service import WindowsService
from src.utils import utils_mail, utils_path
from src.utils.my_logger import my_logger as logger
from src.utils.utils_time import UtilsTime


class OnmyojiController:
    @staticmethod
    def create_execute_tasks(game_device_id: str, game_id: str, projects_num: str = None, project_name: str = None,
                             project_num: str = None, game_round: str = 1, relation_num: str = 1,
                             project_num_times: {} = None, start_hour: int = 0, end_hour: int = 23):
        # 设备信息
        game_device = GameDevices(Mapper.select_game_devices(game_device_id))
        # 创建项目信息
        if projects_num:
            game_tasks = MapperExtend.select_game_task("", projects_num)
        else:
            game_tasks = OnmyojiController.create_tasks(game_id, project_num, project_name,
                                                        project_num_times)
        # 添加设备信息
        for i in range(len(game_tasks)):
            game_task = game_tasks[i]
            game_projects = GameProjects(game_task[0])
            game_projects_relation = GameProjectsRelation(game_task[1])
            game_account = GameAccount(game_task[2])
            game_project = GameProject(game_task[3])
            game_task = [game_projects, game_projects_relation, game_account, game_project, game_device]
            game_tasks[i] = game_task
        # 执行任务
        OnmyojiController.execute_tasks(game_tasks, game_round, relation_num, start_hour, end_hour)

    @staticmethod
    def create_tasks(game_ids: str, project_num: str, project_name: str,
                     project_num_times: {} = None):
        # 初始化任务信息
        task = []
        game_ids_list = []
        project_num_list = []
        num = 0
        if game_ids is not None:
            game_ids_list = game_ids.split(',')
        if project_num:
            project_num_list = project_num.split(',')
        elif not project_num and project_name:
            project_name_list = project_name.split(',')
            for i_num in range(len(project_name_list)):
                project_number = GameProject(MapperExtend.select_game_project("", "", project_name_list[i_num])[0])
                project_num_list.append(project_number.project_num)
        for i in range(len(game_ids_list)):
            game_id = game_ids_list[i]
            game_projects = GameProjects()
            game_projects_relation = GameProjectsRelation()
            game_account = GameAccount(Mapper.select_game_account(game_id))
            for j in range(len(project_num_list)):
                game_project = GameProject(MapperExtend.select_game_project("", project_num_list[j])[0])
                game_projects_relation.relation_num = num + 1
                if project_num_times:
                    game_projects_relation.project_num_times = project_num_times[game_project.project_name]
                game_task = [game_projects, game_projects_relation, game_account, game_project]
                day = UtilsTime.get_day_str()
                region_over = MapperExtend.select_region_over(day, game_id)
                if not region_over and game_project.project_name == "阴阳寮突破":
                    logger.info("{}：{},阴阳寮突破进度100%,跳过创建该任务", day, game_account.role_name)
                    continue
                task.append(game_task)
            num = num + 1
        return task

    @staticmethod
    def execute_tasks(game_tasks: [], game_round: str, relation_num: str, start_hour: int = 0,
                      end_hour: int = 23) -> None:
        """
        项目组任务
        :param game_tasks: 项目组信息
        :param game_round: 项目组执行次数
        :param relation_num:  项目组中断后重新执行的序号
        :param start_hour:开始时间
        :param end_hour: 结束时间
        :return: None
        """
        try:
            time_start = time.time()
            path1 = os.path.join(utils_path.get_project_path_log(), "info")
            WindowsService.delete_folder_file(path1, 2)
            path2 = os.path.join(utils_path.get_project_path_log(), "debug")
            WindowsService.delete_folder_file(path2, 2)
            if len(game_tasks) > 0:
                logger.info("任务开始")
                # 循环项目组
                for i in range(int(game_round)):
                    logger.info("第{}轮", i + 1)
                    # 循环项目
                    for j in range(len(game_tasks)):
                        time_task_start = time.time()
                        game_task = game_tasks[j]
                        game_projects_relation = GameProjectsRelation(game_task[1])
                        game_account = GameAccount(game_task[2])
                        game_project = GameProject(game_task[3])
                        game_device = GameDevices(game_task[4])
                        # 获取当前时间
                        current_time1 = datetime.datetime.now()
                        # 获取当前时间的小时数
                        current_hour = current_time1.hour
                        if (game_projects_relation.relation_num >= int(relation_num)
                                and (start_hour <= current_hour <= end_hour)):
                            logger.info("{},{}:{}", game_projects_relation.relation_num, game_project.project_name,
                                        game_account.role_name)
                            logger.debug("当前状态初始化")
                            ImageService.auto_setup(game_device.id)
                            is_initialization = OnmyojiService.initialization(game_task)
                            if not is_initialization:
                                # 如果是云手机，重启云手机，重新授权，重新初始化（待定）
                                logger.debug("当前状态初始化失败，重新初始化")
                                is_initialization = OnmyojiService.initialization(game_task)
                            # 判断项目名称，根据项目名称执行不同的函数
                            if is_initialization:
                                # 项目 1、24 每日奖励领取
                                if game_project.project_name in ["登录"]:
                                    OnmyojiService.initialization(game_task)
                                # 项目 2
                                elif game_project.project_name in ["每日奖励"]:
                                    OnmyojiService.daily_rewards(game_task)
                                # 项目 3
                                elif game_project.project_name in ["逢魔之时"]:
                                    OnmyojiService.encounter_demons(game_task)
                                # 项目 4
                                elif game_project.project_name in ["地域鬼王"]:
                                    OnmyojiService.ghost_king(game_task)
                                # 项目 5
                                elif game_project.project_name in ["式神寄养"]:
                                    OnmyojiService.foster_care(game_task)
                                # 项目 5
                                elif game_project.project_name in ["阴阳寮管理"]:
                                    OnmyojiService.shack_house(game_task)
                                # 项目 7
                                elif game_project.project_name in ["阴阳寮突破"]:
                                    # 获取本日阴阳寮是否已攻破，，5-24 检查本日 05 检查昨日，已攻破则跳过，不执行项目
                                    day = UtilsTime.get_day_str()
                                    region_over = MapperExtend.select_region_over(day, game_account.id)
                                    if not region_over and game_project.project_name == "阴阳寮突破":
                                        logger.info("{}：{},阴阳寮突破进度100%,跳过执行该任务", day,
                                                    game_account.role_name)
                                        continue
                                    OnmyojiService.region_border(game_task)
                                    if (game_projects_relation.wait_after_time
                                            and game_projects_relation.wait_after_time > 0):
                                        time_time = game_projects_relation.wait_after_time
                                        logger.debug("战斗结束后等待一段时间")
                                        result_time = random.randint(time_time - 5, time_time + 5)
                                        logger.debug("等待{}分钟", result_time)
                                        time.sleep(result_time * 60)
                                # 项目 8
                                elif game_project.project_name in ["个人突破"]:
                                    OnmyojiService.border_fight(game_task)
                                # 项目 9
                                elif game_project.project_name in ["好友管理"]:
                                    OnmyojiService.friends_manage(game_task)
                                # 项目 10
                                elif game_project.project_name in ["好友协战"]:
                                    OnmyojiService.friends_fight(game_task)
                                # 项目 11
                                elif game_project.project_name in ["觉醒十"]:
                                    OnmyojiService.awakening(game_task)
                                # 项目 12,13,14,15
                                elif game_project.project_name in ["魂一", "魂十", "魂十一", "魂十二"]:
                                    OnmyojiService.soul_fight(game_task)
                                # 项目 16
                                elif game_project.project_name in ["业原火"]:
                                    OnmyojiService.soul_fight_fire(game_task)
                                # 项目 17
                                elif game_project.project_name in ["日轮之陨"]:
                                    OnmyojiService.soul_fight_sun(game_task)
                                # 项目 18
                                elif game_project.project_name in ["永生之海"]:
                                    OnmyojiService.soul_fight_sea(game_task, 1)
                                # 项目 19
                                elif game_project.project_name in ["斗技"]:
                                    OnmyojiService.pvp(game_task)
                                # 项目 20
                                elif game_project.project_name in ["御魂整理"]:
                                    OnmyojiService.soul_arrange(game_task)
                                # 项目 21
                                elif game_project.project_name in ["探索"]:
                                    OnmyojiService.explore_chapters(game_task)
                                # 项目 22
                                elif game_project.project_name in ["御灵"]:
                                    OnmyojiService.spirit_fight(game_task)
                                # 项目 23
                                elif game_project.project_name in ["契灵"]:
                                    OnmyojiService.deed_spirit(game_task)
                            else:
                                logger.info("当前状态初始化失败2次{}，不执行项目", game_account.role_name)
                            time_end = time.time()
                            logger.info("{}:{},项目执行时间{}.项目组累计执行时间{}", game_account.role_name,
                                        game_project.project_name,
                                        UtilsTime.convert_seconds(time_end - time_task_start),
                                        UtilsTime.convert_seconds(time_end - time_start))
        except Exception as e:
            utils_mail.send_email("阴阳师脚本", "异常", e)
            logger.exception(e)
