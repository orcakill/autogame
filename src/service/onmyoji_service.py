# @Time: 2023年05月31日 17:51
# @Author: orcakill
# @File: onmyoji_service.py
# @Description: 服务接口

from src.service_onmyoji_impl import impl_border, impl_friends, impl_ghost, impl_reward, impl_awakening, impl_soul, \
    impl_initialization, impl_explore
from src.service_onmyoji_impl import impl_house


class OnmyojiService:

    @staticmethod
    def initialization(game_task: []):
        """
        项目1 当前状态初始化
        :param game_task: 任务信息
        :return:
        """
        return  impl_initialization.initialization(game_task)

    @staticmethod
    def soul_fight(game_task: []):
        """
        御魂战斗  八岐大蛇
        魂一  第一次战斗检查协战，有协战上协战，没协战直接退出到首页，不开加成
        魂十  第一次战斗检查协战，有协战上协战，开加成，
        魂十一  不检查协战，不上协战，开加成
        :param game_task: 项目组信息
        :return:
        """
        impl_soul.soul_fight(game_task)

    @staticmethod
    def border_fight(game_task: [], fight_times: int = 40):
        """
        结界突破 border
        :param fight_times: 默认战斗次数40
        :param game_task: 项目信息
        :return:
        """
        impl_border.border_fight(game_task, fight_times)

    @staticmethod
    def awakening(game_task: [], awakening_type: int = 0):
        """
            觉醒十 风、火、水、雷（默认雷）  开加成，选觉醒阵容
            :param awakening_type: 默认类型
            :param game_task:  任务信息
            :return:
            """
        impl_awakening.awakening(game_task, awakening_type)

    @staticmethod
    def daily_rewards(game_task: []):
        """
        每日奖励
        :param game_task: 任务信息
        :return:
        """
        impl_reward.daily_rewards(game_task)

    @staticmethod
    def encounter_demons(game_task: []):
        """
        逢魔之时
        :param game_task: 任务信息
        :return:
        """
        impl_ghost.encounter_demons(game_task)

    @staticmethod
    def ghost_king(game_task: []):
        """
        地域鬼王
        :param game_task:
        :return:
        """
        impl_ghost.ghost_king(game_task)

    @staticmethod
    def friends_manage(game_task: []):
        """
        好友管理
        :param game_task:
        :return:
        """
        impl_friends.friends_manage(game_task)

    @staticmethod
    def friends_fight(game_task: []):
        """
        好友协战
        :param game_task:
        :return:
        """
        impl_friends.friends_fight(game_task)

    @staticmethod
    def foster_care(game_task: []):
        """
        式神寄养
        :param game_task:
        :return:
        """
        impl_house.foster_care(game_task)

    @staticmethod
    def region_border(game_task: []):
        """
        阴阳寮突破
        :param game_task: 任务信息
        :return:
        """
        impl_border.region_border(game_task)

    @staticmethod
    def shack_house(game_task: []):
        """
        阴阳寮管理
        :param game_task: 阴阳寮管理
        :return:
        """
        impl_house.shack_house(game_task)

    @staticmethod
    def explore_chapters(game_task: []):
        """
        阴阳寮管理
        :param game_task: 阴阳寮管理
        :return:
        """
        impl_explore.explore_chapters(game_task)
