# @Time: 2023年05月31日 17:51
# @Author: orcakill
# @File: onmyoji_service.py
# @Description: 服务接口

from src.service_onmyoji_impl import impl_border, impl_friends, impl_ghost, impl_reward, impl_awakening, impl_soul, \
    impl_initialization, impl_explore, impl_pvp, impl_spirit, impl_deed
from src.service_onmyoji_impl import impl_house


class OnmyojiService:

    @staticmethod
    def initialization(game_task: []):
        """
        项目1 当前状态初始化
        :param game_task: 项目信息
        :return:
        """
        return impl_initialization.initialization(game_task)

    @staticmethod
    def soul_fight(game_task: []):
        """
        御魂战斗  八岐大蛇
        魂一  第一次战斗检查协战，有协战上协战，没协战直接退出到首页，不开加成
        魂十  第一次战斗检查协战，有协战上协战，开加成，
        魂十一  不检查协战，不上协战，开加成
        :param game_task: 项目信息
        :return:
        """
        impl_soul.soul_fight(game_task)

    @staticmethod
    def border_fight(game_task: [], fight_times: int = 40):
        """
        结界突破 border
        :param fight_times: 默认战斗次数40
        :param game_task: 项目组信息
        :return:
        """
        impl_border.border_fight(game_task, fight_times)

    @staticmethod
    def awakening(game_task: [], awakening_type: int = 0):
        """
            觉醒十 风、火、水、雷（默认雷）  开加成，选觉醒阵容
            :param awakening_type: 默认类型
            :param game_task:  项目组信息
            :return:
            """
        impl_awakening.awakening(game_task, awakening_type)

    @staticmethod
    def daily_rewards(game_task: []):
        """
        每日奖励
        :param game_task: 项目信息
        :return:
        """
        impl_reward.daily_rewards(game_task)

    @staticmethod
    def encounter_demons(game_task: []):
        """
        逢魔之时
        :param game_task: 项目信息
        :return:
        """
        impl_ghost.encounter_demons(game_task)

    @staticmethod
    def ghost_king(game_task: []):
        """
        地域鬼王
        :param game_task:项目信息
        :return:
        """
        impl_ghost.ghost_king(game_task)

    @staticmethod
    def friends_manage(game_task: []):
        """
        好友管理
        :param game_task:项目信息
        :return:
        """
        impl_friends.friends_manage(game_task)

    @staticmethod
    def friends_fight(game_task: []):
        """
        好友协战
        :param game_task:项目信息
        :return:
        """
        impl_friends.friends_fight(game_task)

    @staticmethod
    def foster_care(game_task: []):
        """
        式神寄养
        :param game_task:项目信息
        :return:
        """
        impl_house.foster_care(game_task)

    @staticmethod
    def region_border(game_task: []):
        """
        阴阳寮突破
        :param game_task: 项目信息
        :return:
        """
        impl_border.region_border(game_task)

    @staticmethod
    def shack_house(game_task: []):
        """
        阴阳寮管理
        :param game_task: 项目信息
        :return:
        """
        impl_house.shack_house(game_task)

    @staticmethod
    def soul_fight_fire(game_task: []):
        """
        业原火 三层
        :param game_task: 项目信息
        :return:
        """
        impl_soul.soul_fight_fire(game_task)

    @staticmethod
    def soul_fight_sun(game_task: []):
        """
        日轮之陨 三层
        :param game_task: 项目信息
        :return:
        """
        impl_soul.soul_fight_sun(game_task)

    @staticmethod
    def soul_fight_sea(game_task: [], fight: int = 0):
        """
        永生之海 四层
        :param fight:战斗开关，0 为根据掉落御魂时间来  1强制战斗
        :param game_task: 项目信息
        :return:
        """
        impl_soul.soul_fight_sea(game_task, fight=fight)

    @staticmethod
    def pvp(game_task: []):
        """
        斗技 名士以下
        :param game_task: 项目信息
        :return:
        """
        impl_pvp.pvp(game_task)

    @staticmethod
    def explore_chapters(game_task: [], chapter: int = 28, difficulty: int = 1):
        """
        章节探索
        :param difficulty: 难度
        :param chapter: 章节
        :param game_task: 项目信息
        :return:
        """
        impl_explore.explore_chapters(game_task, chapter, difficulty)

    @staticmethod
    def spirit_fight(game_task: []):
        """
        御灵战斗
        :param game_task: 项目信息
        :return:
        """
        impl_spirit.spirit_fight(game_task)

    @staticmethod
    def soul_arrange(game_task: []):
        """
        御魂整理
        :param game_task: 项目信息
        :return:
        """
        impl_reward.soul_arrange(game_task)

    @staticmethod
    def deed_spirit(game_task: []):
        """
        契灵
        :param game_task: 项目信息
        :return:
        """
        impl_deed.deed_spirit(game_task)
