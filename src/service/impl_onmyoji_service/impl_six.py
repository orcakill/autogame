"""
# @Time: 2023年11月30日17:51
# @Author: orcakill
# @File: impl_six.py
# @Description: 六道之门(月之海)
"""
import time
from collections import Counter

from tornado import concurrent

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji
from src.model.models import GameAccount, GameProject, GameDevice, GameProjectsRelation, GameProjectLog
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_onmyoji_service import impl_initialization
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def sea_moon(game_task: []):
    # 开始时间
    time_start = time.time()
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevice(game_task[4]))
    #  战斗次数
    fight_times = game_projects_relation.project_num_times
    if fight_times is None:
        fight_times = 1
    # 最终评价
    evaluate = ''
    logger.debug("检查是否是六道之门-月之海首页")
    is_home = ImageService.exists(Onmyoji.six_moon_YZHSY)
    is_open = ImageService.exists(Onmyoji.six_moon_WFXQ)
    if not is_home or not is_open:
        logger.debug("当前不是六道之门-月之海首页")
        logger.debug("拒接协战")
        ComplexService.refuse_reward()
        logger.debug("探索")
        ImageService.touch(Onmyoji.home_TS)
        logger.debug("六道之门入口")
        ImageService.touch(Onmyoji.six_moon_LDZMRK)
        logger.debug("月之海入口")
        is_six_moon = ImageService.touch(Onmyoji.six_moon_YZHRK)
        if not is_six_moon:
            logger.debug("无月之海入口，更替")
            ImageService.touch(Onmyoji.six_moon_GT)
            logger.debug("选择月之海")
            ImageService.touch(Onmyoji.six_moon_XZYZH)
            logger.debug("重新点击月之海入口")
            ImageService.touch(Onmyoji.six_moon_YZHRK)
        logger.debug("重新检查是否是六道之门-月之海首页")
        is_home = ImageService.exists(Onmyoji.six_moon_YZHSY)
        is_open = ImageService.exists(Onmyoji.six_moon_WFXQ)
    is_diagram = ImageService.exists(Onmyoji.six_moon_YZHJT)
    if is_home and is_open and is_diagram:
        logger.debug("月之海首页")
        for i in range(fight_times):
            # 重置结果
            current_result = []
            logger.debug("第{}次月之海", i + 1)
            logger.debug("开启")
            is_start = ImageService.touch(Onmyoji.six_moon_KQ)
            if not is_start:
                logger.debug("无开启，点击继续")
                ImageService.touch(Onmyoji.six_moon_JX)
            if is_start:
                logger.debug("确定")
                ImageService.touch(Onmyoji.six_moon_QD)
                logger.debug("60体力开启")
                ImageService.touch(Onmyoji.six_moon_KQ60TL)
                logger.debug("选择柔风抱暖")
                ComplexService.touch_two(Onmyoji.six_moon_JN_RFBN, Onmyoji.six_moon_XZJN)
            current_result.append(("技能", deal_name(Onmyoji.six_moon_JN_RFBN)))
            for i_fight in range(20):
                logger.debug("第{}回合", i_fight + 1)
                logger.debug("当前秘宝")
                current_count(current_result, "秘宝")
                logger.debug("当前技能")
                current_count(current_result, "技能")
                logger.debug("回合事件")
                if i_fight < 5:
                    current_result = deal_event("月之海", current_result, 1)
                else:
                    current_result = deal_event("月之海", current_result, 4)
                if current_exist(current_result, "事件", deal_name(Onmyoji.six_moon_YXXZ)):
                    logger.debug("月之海结束")
                    break
            logger.debug("最终评价:")
            if current_exist(current_result, "评价", deal_name(Onmyoji.six_moon_PJ_J)):
                evaluate = deal_name(Onmyoji.six_moon_PJ_J)
            else:
                evaluate = "其它"
            logger.debug(evaluate)
            logger.debug(current_result)
            logger.debug("事件耗时")
            current_all(current_result, "事件")
    logger.debug("返回首页")
    ImageService.touch(Onmyoji.comm_FH_ZSJALYXBSXYH)
    ImageService.touch(Onmyoji.comm_FH_ZSJALYXBSXYH)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    # 结束时间
    time_end = time.time()
    # 总用时
    time_all = time_end - time_start
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='月之海-' + evaluate, cost_time=int(time_all))
    Mapper.save_game_project_log(game_project_log)
    logger.debug("本次月之海，总用时{}秒", UtilsTime.convert_seconds(time_all))


def deal_event(six_type: str, current_result: [], refresh_count: int = 4):
    """
        回合事件及选择技能
    :param six_type: 六道之门类型
    :param current_result: 秘宝、技能、最终评价
    :param refresh_count: 刷新次数
    :return:
    """
    time_start = time.time()
    # 事件集合
    event_list = []
    # 技能集合
    skill_list = []
    # 技能文字集合
    skill_word_list = []
    # 秘宝集合
    rare_list = []
    # 神秘事件
    mysterious_list = []
    # 混沌事件集合
    chaos_list = []
    # 评价集合
    evaluate_list = []
    if six_type == "月之海":
        # 月之海，回合事件，按月晓星征、星之屿、鏖战、神秘、混沌、宁息的优先级
        event_list = [Onmyoji.six_moon_YXXZ, Onmyoji.six_moon_SJ_XZY, Onmyoji.six_moon_SJ_SM,
                      Onmyoji.six_moon_SJ_HD, Onmyoji.six_moon_SJ_NX, Onmyoji.six_moon_SJ_AZ]
        # 月之海，技能+优先级+当前等级，按柔风抱暖、六道暴虐、细雨化屏、妖力化身选取
        skill_list = [Onmyoji.six_moon_JN_RFBN, Onmyoji.six_moon_JN_LDBN, Onmyoji.six_moon_JN_YLHS,
                      Onmyoji.six_moon_JN_XYHP]
        # 月之海，技能文字+优先级+当前等级，按柔风抱暖、六道暴虐、细雨化屏、妖力化身选取
        skill_word_list = [Onmyoji.six_moon_JNWZ_RFBN, Onmyoji.six_moon_JNWZ_LDBN, Onmyoji.six_moon_JNWZ_XYHP,
                           Onmyoji.six_moon_JNWZ_YLHS]
        # 月之海，秘宝,攻击御守，火之卷
        rare_list = [Onmyoji.six_moon_MB_GJYS, Onmyoji.six_moon_MB_HZJ]
        # 月之海，混沌事件，幸运宝盒,精英
        chaos_list = [Onmyoji.six_moon_HDSJ_XYBX, Onmyoji.six_moon_HDSJ_JY]
        # 月之海，神秘事件，背包仿造。技能转换
        mysterious_list = [Onmyoji.six_moon_SMSJ_BBFZ, Onmyoji.six_moon_SMSJ_JNZH]
        # 评价 极特优良
        evaluate_list = [Onmyoji.six_moon_PJ_J]
    logger.debug("检查当前事件")
    ComplexService.refuse_reward()
    event = check_list(event_list)
    event1 = ''
    if event is None:
        logger.debug("重新检查当前事件")
        ComplexService.refuse_reward()
        event = check_list(event_list)
    if event == Onmyoji.six_moon_SJ_AZ:
        logger.debug("当前事件：鏖战")
        is_fight = ImageService.touch(Onmyoji.six_moon_SJ_AZ, rgb=True)
        if not is_fight:
            ImageService.touch(Onmyoji.six_moon_SJ_AZ, rgb=True)
        if is_fight:
            logger.debug("点击右侧普通")
            ImageService.touch(Onmyoji.six_moon_PT, timeouts=10)
            logger.debug("点击挑战")
            ImageService.touch(Onmyoji.six_moon_TZ)
            logger.debug("等待战斗结束")
            ImageService.exists(Onmyoji.six_moon_WXZC, timeouts=90)
            logger.debug("选择技能")
            skill = select_skills(skill_list, refresh_count, "技能")
            if skill:
                current_result.append(("技能", deal_name(skill)))
            logger.debug("获取奖励")
            ImageService.touch(Onmyoji.six_moon_HDJL)
    if event == Onmyoji.six_moon_SJ_XZY:
        logger.debug("当前事件：星之屿")
        ImageService.touch(Onmyoji.six_moon_SJ_XZY)
        logger.debug("点击星之子")
        ImageService.touch(Onmyoji.six_moon_XZZ)
        logger.debug("点击挑战")
        ImageService.touch(Onmyoji.six_moon_TZ)
        logger.debug("等待战斗结束")
        ImageService.exists(Onmyoji.six_moon_WXZC, timeouts=60)
        logger.debug("选择秘宝")
        rare = select_skills(rare_list, 4, "秘宝")
        if rare:
            current_result.append(("秘宝", deal_name(rare)))
        logger.debug("选择技能")
        skill = select_skills(skill_list, refresh_count, "技能")
        if skill:
            current_result.append(("技能", deal_name(skill)))
        logger.debug("获取奖励")
        ImageService.touch(Onmyoji.six_moon_HDJL)
    if event == Onmyoji.six_moon_SJ_HD:
        logger.debug("当前事件：混沌")
        ImageService.touch(Onmyoji.six_moon_SJ_HD)
        logger.debug("检查混沌事件")
        event1 = check_list(chaos_list)
        if event1 is None:
            logger.debug("重新检查混沌事件")
            event1 = check_list(chaos_list)
        if event1 == Onmyoji.six_moon_HDSJ_XYBX:
            logger.debug("混沌事件：幸运宝盒")
            logger.debug("检查当前技能数")
            skill_counts = current_counts(current_result, "技能")
            logger.debug("当前技能数{}", skill_counts)
            if skill_counts == 4:
                logger.debug("技能数等于4,点击幸运宝盒")
                ImageService.touch(Onmyoji.six_moon_HDSJ_XYBX)
                logger.debug("点击开启")
                ImageService.touch(Onmyoji.six_moon_KQ)
                logger.debug("点击获得奖励")
                ImageService.touch(Onmyoji.six_moon_HDJL)
            else:
                logger.debug("技能数小于4，点击离开")
                logger.debug("点击离开")
                ImageService.touch(Onmyoji.six_moon_LK)
        if event1 == Onmyoji.six_moon_HDSJ_JY:
            logger.debug("混沌事件：精英")
            ImageService.touch(Onmyoji.six_moon_SJ_XZY)
            logger.debug("点击精英")
            ImageService.touch(Onmyoji.six_moon_HDSJ_JY)
            logger.debug("点击挑战")
            ImageService.touch(Onmyoji.six_moon_TZ)
            logger.debug("等待战斗结束")
            ImageService.exists(Onmyoji.six_moon_WXZC, timeouts=60)
            logger.debug("选择技能")
            rare = select_skills(skill_list, refresh_count, "技能")
            if rare:
                current_result.append(("技能", deal_name(rare)))
            logger.debug("选择技能")
            skill = select_skills(skill_list, refresh_count, "技能")
            if skill:
                current_result.append(("技能", deal_name(skill)))
            logger.debug("获取奖励")
            ImageService.touch(Onmyoji.six_moon_HDJL)
    if event == Onmyoji.six_moon_SJ_NX:
        logger.debug("当前事件：宁息")
        ImageService.touch(Onmyoji.six_moon_SJ_NX)
        logger.debug("购买技能")
        for i_buy in range(len(skill_word_list)):
            logger.debug("第{}次购买，{}", i_buy + 1, skill_word_list[i_buy])
            ImageService.touch(skill_word_list[i_buy])
            logger.debug("点击确定")
            is_buy = ImageService.touch(Onmyoji.six_moon_TYQD)
            if is_buy:
                current_result.append(("技能", deal_name(skill_word_list[i_buy])))
        logger.debug("点击离开")
        ImageService.touch(Onmyoji.six_moon_LK)
    if event == Onmyoji.six_moon_SJ_SM:
        logger.debug("当前事件：神秘")
        ImageService.touch(Onmyoji.six_moon_SJ_SM)
        logger.debug("检查神秘事件")
        event1 = check_list(mysterious_list)
        if event1 == Onmyoji.six_moon_SMSJ_BBFZ:
            logger.debug("神秘事件：背包仿造")
            for i_create in range(len(skill_list)):
                logger.debug("第{}次仿造,仿造技能 {}", i_create + 1, skill_list[i_create])
                ImageService.touch(skill_list[i_create])
                logger.debug("点击仿造")
                ImageService.touch(Onmyoji.six_moon_FZ)
                logger.debug("点击确定")
                ImageService.touch(Onmyoji.six_moon_TYQD)
                logger.debug("点击仿造成功")
                is_true = ImageService.touch(Onmyoji.six_moon_FZCG)
                if is_true:
                    current_result.append(("技能", deal_name(skill_word_list[i_create])))
                    logger.debug("仿造结束")
                    break
        if event1 == Onmyoji.six_moon_SMSJ_JNZH:
            logger.debug("神秘事件：技能转换")
            logger.debug("点击返回")
            ImageService.touch(Onmyoji.comm_FH_ZSJALYXBSXYH)
    if event == Onmyoji.six_moon_YXXZ:
        logger.debug("当前事件：月晓星征")
        ImageService.touch(Onmyoji.six_moon_YXXZ)
        logger.debug("点击挑战")
        ImageService.touch(Onmyoji.six_moon_TZ)
        logger.debug("检查自动战斗")
        is_auto = ImageService.exists(Onmyoji.six_moon_ZDZD)
        if is_auto:
            logger.debug("自动战斗中")
            for auto in range(20):
                logger.debug("点击秘宝")
                ImageService.touch(Onmyoji.six_moon_SLZMB)
                is_reward = ImageService.exists(Onmyoji.six_moon_SLZHDJL)
                if is_reward:
                    logger.debug("战斗结束")
                    break
                time.sleep(3)
        logger.debug("获得奖励")
        ComplexService.get_reward(Onmyoji.six_moon_SLZHDJL)
        is_blank = ImageService.exists(Onmyoji.six_moon_DJKB)
        if not is_blank:
            logger.debug("获得经验")
            ImageService.touch(Onmyoji.six_moon_HDJY)
            logger.debug("技能解锁")
            ImageService.touch(Onmyoji.six_moon_JNJS)
            logger.debug("点击使用")
            ImageService.touch(Onmyoji.six_moon_SY)
        logger.debug("检查评价")
        evaluate = check_list(evaluate_list)
        if evaluate:
            current_result.append(("评价", deal_name(evaluate)))
        logger.debug("点击空白")
        ImageService.touch(Onmyoji.six_moon_DJKB)
    time_end = time.time()
    time_all = time_end - time_start
    logger.debug("本回合事件{},{},用时{}", deal_name(event), deal_name(event1), UtilsTime.convert_seconds(time_all))
    current_result.append(("事件", deal_name(event), deal_name(event1), time_all))
    return current_result


def select_skills(skill_list: [], refresh_count: int = 4, skill_type: str = "秘宝"):
    """
    选择技能或秘宝
    :param skill_type: 类型
    :param skill_list: 技能列表
    :param refresh_count: 刷新次数
    :return:
    """
    skill = ''
    for i in range(refresh_count):
        if i > 0:
            logger.debug("无目标{}，点击刷新", skill_type)
            ImageService.touch(Onmyoji.six_moon_SXMB)
        logger.debug("第{}次选择{}", i + 1, skill_type)
        skill = check_list(skill_list)
        if skill == Onmyoji.six_moon_MB_GJYS:
            logger.debug("当前秘宝攻击御守，需要再次检查")
            is_again = ImageService.exists(Onmyoji.six_moon_MB_GJYSWZ)
            if not is_again:
                skill = None
                logger.debug("检查是否有火之卷")
                is_skill = ImageService.exists(Onmyoji.six_moon_MB_HZJ)
                if is_skill:
                    skill = Onmyoji.six_moon_MB_HZJ
        if skill == Onmyoji.six_moon_MB_HZJ:
            logger.debug("当前秘宝火之卷，需要再次检查")
            is_again = ImageService.exists(Onmyoji.six_moon_MB_HZJWZ)
            if not is_again:
                skill = None
        if skill and skill is not None:
            logger.debug("选择{}", skill)
            ComplexService.touch_two(skill, Onmyoji.six_moon_XZJN)
            logger.debug("选择完成")
            break
        if i == refresh_count - 1:
            logger.debug("最终检查无目标{}，选择万相之赐", skill_type)
            ComplexService.touch_two(Onmyoji.six_moon_WXZC, Onmyoji.six_moon_XZJN, rgb1=False)
    return skill


def check_list(image_list: []):
    def check_image(num, image):
        logger.debug("{} {}", num, image)
        is_num = ImageService.exists(image, rgb=True)
        if is_num:
            return num
        return 99

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_image, i, image_list[i]) for i in range(len(image_list))]
    results = [future.result() for future in futures]
    min_value = min(results)
    if min_value != 99:
        return image_list[min_value]
    return None


def current_count(current_list: [], count_type):
    skill = []
    for i in range(len(current_list)):
        event = current_list[i]
        if event[0] == count_type:
            skill.append(event[1])
    skill_result = Counter(skill)
    for key, value in skill_result.items():
        logger.debug(f'--{key}: {value}')


def current_counts(current_list: [], count_type):
    """
    判断当前技能数
    :param current_list: 集合
    :param count_type:类型
    :return:
    """
    skill = []
    for i in range(len(current_list)):
        list1 = current_list[i]
        if list1[0] == count_type:
            skill.append(list1[1])
    skill_result = Counter(skill)
    return len(skill_result)


def current_exist(current_list: [], count_type: str, name: str):
    for i in range(len(current_list)):
        event = current_list[i]
        if event[0] == count_type:
            if event[1] == name:
                return True
    return False


def current_all(current_list: [], count_type: str):
    for i in range(len(current_list)):
        event = current_list[i]
        if event[0] == count_type:
            logger.debug(current_list[i])


def deal_name(s: str):
    if s is not None:
        return s.split("\\")[-1]
    return None
