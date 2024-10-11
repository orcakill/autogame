# @Time: 2023年09月11日 10:30
# @Author: orcakill
# @File: impl_explore.py
# @Description: 探索
import time

from src.dao.mapper import Mapper
from src.model.enum import Onmyoji, Cvstrategy
from src.model.models import GameProjectsRelation, GameAccount, GameDevice, GameProject, GameProjectLog
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_onmyoji_service import impl_initialization
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def explore_chapters(game_task: [], chapter: int = 28, difficulty: int = 1):
    """
    章节探索
    默认选择28章困难
    自动添加候补式神
    全打 打3次，有小怪打小怪，有boss打boss，都没有左右移动，检查不到小怪和boss，退出探索
    :param difficulty: 难度 0 普通 1 困难
    :param chapter: 默认28章
    :param game_task:
    :return:
    """
    # 项目信息
    (game_projects_relation, game_account,
     game_project, game_devices) = (GameProjectsRelation(game_task[1]), GameAccount(game_task[2]),
                                    GameProject(game_task[3]), GameDevice(game_task[4]))
    # 开始时间
    time_start = time.time()
    # 战斗胜利次数
    num_win = 0
    # 战斗失败次数
    num_false = 0
    # 战斗用时列表
    time_fight_list = []
    # 轮次战斗用时列表
    time_round_list = []
    # 章节首页
    chapter_home = None
    # 章节层数
    chapter_layers = None
    # 默认战斗轮次
    fight_times = 20
    if game_projects_relation.project_num_times:
        if game_projects_relation.project_num_times > 0:
            fight_times = game_projects_relation.project_num_times
    if chapter == 28:
        chapter_home, chapter_layers = Onmyoji.explore_ZJSY_28, Onmyoji.explore_ZJ_28
    elif chapter == 7:
        chapter_home, chapter_layers = Onmyoji.explore_ZJSY_7, Onmyoji.explore_ZJ_7
    elif chapter == 13:
        chapter_home, chapter_layers = Onmyoji.explore_ZJSY_13, Onmyoji.explore_ZJ_13
    # 获取设备分辨率
    resolution = ImageService.resolution_ratio()
    # 默认未自动轮换
    is_rotation = False
    logger.debug("章节探索-开始")
    # 章节探索
    for i in range(1, fight_times + 1):
        time_round_start = time.time()
        logger.debug("第{}轮章节探索", i)
        logger.debug("判断是否是章节首页")
        is_home = ImageService.exists(chapter_home)
        if not is_home:
            logger.debug("拒接协战")
            ComplexService.refuse_reward()
            ComplexService.refuse_reward()
            logger.debug("探索界面-判断是否是探索界面")
            is_explore = ImageService.exists(Onmyoji.soul_BQ_YHTB)
            if is_explore:
                logger.debug("探索界面，判断左侧宝箱")
                is_treasure_chest = ImageService.touch(Onmyoji.explore_ZCBX)
                if is_treasure_chest:
                    logger.debug("领取奖励")
                    ImageService.touch(Onmyoji.explore_TCTZ)
                logger.debug("选择章节")
                ImageService.touch(chapter_layers)
                if difficulty == 1:
                    logger.debug("选择困难")
                    ImageService.touch(Onmyoji.explore_ZJNDKN)
                else:
                    logger.debug("选择普通")
                    ImageService.touch(Onmyoji.explore_ZJNDPT)
            logger.debug("首页-判断是否有探索")
            is_explore = ImageService.exists(Onmyoji.home_TS)
            if is_explore:
                logger.debug("点击探索")
                ImageService.touch(Onmyoji.home_TS)
                logger.debug("选择章节")
                if chapter == 28:
                    is_select_chapter = select_chapter()
                    if not is_select_chapter:
                        logger.debug("切换文字识别")
                        ImageService.ocr_touch("第二十八章")
                else:
                    ImageService.touch(chapter_layers)
                logger.debug("选择困难")
                ImageService.touch(Onmyoji.explore_ZJNDKN)
        if not is_home:
            logger.debug("重新检查章节首页")
            is_home = ImageService.exists(chapter_home)
        if not is_home:
            logger.debug("不在章节首页，进入下一次章节探索")
        else:
            logger.debug("进入章节探索战斗")
            ImageService.touch(Onmyoji.explore_ZJTS, timeouts=10)
            logger.debug("准备完成，开始战斗")
            # 默认无boss
            is_boss = False
            for i_fight in range(1, 12):
                time_fight_start = time.time()
                logger.debug("第{}:{}次章节探索战斗", i, i_fight)
                if i_fight > 3:
                    logger.debug("点击首领")
                    is_boss = ImageService.touch(Onmyoji.explore_SLZD)
                if i == 1 and i_fight == 1:
                    logger.debug("添加N卡式神自动轮换")
                    automatic_rotation_type_god()
                    logger.debug("开启经验加成")
                    ComplexService.top_addition(Onmyoji.explore_JC, Onmyoji.explore_JYJC, Onmyoji.explore_JCK,
                                                Onmyoji.explore_JCG, 1)
                if not is_rotation:
                    logger.debug("未自动轮换-锁定阵容")
                    ImageService.touch(Onmyoji.explore_SDZR)
                    logger.debug("未自动轮换-自动轮换")
                    is_rotation = ImageService.touch(Onmyoji.explore_ZDLH)
                if not is_boss:
                    logger.debug("没有首领，点击小怪")
                    for i_little_monster in range(2):
                        is_little_monster = ImageService.touch(Onmyoji.explore_XGZD,deviation=0)
                        if is_little_monster:
                            break
                        else:
                            logger.debug("没有小怪,右移")
                            ImageService.swipe((0.9 * resolution[0], 0.5 * resolution[1]),
                                               (0.1 * resolution[0], 0.5 * resolution[1]))
                            logger.debug("点击中心位置")
                            ImageService.touch_coordinate((0.5 * resolution[0], 0.6 * resolution[1]))
                            logger.debug("进入下一轮循环")
                            continue
                is_auto = ImageService.exists(Onmyoji.explore_ZD)
                if not is_auto:
                    logger.debug("拒接悬赏")
                    ComplexService.refuse_reward()
                    logger.debug("点击可能的准备")
                    is_lock = ImageService.touch(Onmyoji.explore_ZB)
                    if is_lock:
                        logger.debug("点击准备完成，未自动轮换")
                        is_rotation = False
                    logger.debug("点击可能的退出挑战")
                    ImageService.touch(Onmyoji.explore_TCTZ)
                    logger.debug("判断是否存在")
                    logger.debug("跳过本次战斗")
                    continue
                if is_auto:
                    logger.debug("等待战斗结果")
                    is_result = ComplexService.fight_end(Onmyoji.explore_ZDSL, Onmyoji.explore_ZDSB,
                                                         Onmyoji.explore_ZCTZ,
                                                         Onmyoji.explore_TCTZ, Onmyoji.explore_XGZD, None, 40, 2)
                    if is_result in [Onmyoji.explore_ZDSL, Onmyoji.explore_TCTZ]:
                        num_win = num_win + 1
                    elif is_result in [Onmyoji.explore_ZCTZ, Onmyoji.explore_ZDSB]:
                        num_false = num_false + 1
                time_fight_end = time.time()
                time_fight = time_fight_end - time_fight_start
                logger.debug("本次章节探索战斗结束，用时{}秒", round(time_fight, 3))
                time_fight_list.append(time_fight)
                if is_boss:
                    break
            logger.debug("判断是否有式神录")
            is_reward = ImageService.exists(Onmyoji.explore_SSL, wait=5)
            logger.debug("判断章节")
            is_layers = ImageService.exists(chapter_layers)
            if is_reward and not is_layers:
                logger.debug("有式神录，无最后一章,点击左上角返回")
                ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
                logger.debug("确认")
                ImageService.touch(Onmyoji.explore_QR)
            else:
                logger.debug("无式神录")
            time_round_end = time.time()
            time_round_fight = time_round_end - time_round_start
            logger.debug("本次章节探索结束，用时{}秒", round(time_round_fight, 3))
            time_round_list.append(time_round_fight)
            logger.debug("本轮探索战斗结束")
    logger.debug("关闭加成")
    ComplexService.top_addition(Onmyoji.explore_JC, Onmyoji.explore_JYJC, Onmyoji.explore_JCK,
                                Onmyoji.explore_JCG, 0)
    logger.debug("返回首页")
    ImageService.touch(Onmyoji.comm_FH_YSJHDBSCH)
    ImageService.touch(Onmyoji.comm_FH_ZSJLDYXBSXYH)
    logger.debug("确认返回首页")
    impl_initialization.return_home(game_task)
    # 探索-战斗次数
    len_time_fight_list = len(time_fight_list)
    # 探索-战斗轮次
    len_time_round_list = len(time_round_list)
    # 探索-战斗总用时
    time_fight_all = round(sum(time_fight_list))
    # 探索-结束时间
    time_end = time.time()
    # 探索-总用时
    time_all = time_end - time_start
    # 探索-每次战斗平均用时
    time_fight_avg = 0
    if len_time_fight_list > 0:
        time_fight_avg = round(sum(time_fight_list) / len(time_fight_list), 3)
    # 探索-每轮战斗平均用时
    time_round_avg = 0
    if len_time_round_list > 0:
        time_round_avg = round(sum(time_round_list) / len(time_round_list), 3)
    # 记录项目执行结果
    game_project_log = GameProjectLog(project_id=game_project.id, account_id=game_account.id, device_id=game_devices.id,
                                      result='探索', cost_time=int(time_all), fight_time=time_fight_all,
                                      fight_times=len_time_fight_list, fight_win=num_win,
                                      fight_fail=num_false, fight_avg=time_fight_avg)
    Mapper.save_game_project_log(game_project_log)
    logger.debug(
        "{}章探索挑战，总用时{}，共{}轮，每轮平均战斗时间{}，战斗总用时{},每次战斗平均用时{}，挑战{}次，胜利{}次，失败{}次",
        chapter, UtilsTime.convert_seconds(time_all), fight_times, UtilsTime.convert_seconds(time_round_avg),
        UtilsTime.convert_seconds(time_fight_all), time_fight_avg, len_time_fight_list, num_win, num_false)


def select_chapter():
    """
    选择最大章节
    :return:
    """
    results = ImageService.find_all(Onmyoji.explore_ZZ, cvstrategy=Cvstrategy.default)
    if results:
        result = max(results, key=lambda x: x['result'][1])['result']
        if result:
            ImageService.touch_coordinate(result)
            return True
    else:
        logger.debug("找不到章节")
        return False


def automatic_rotation_type_god():
    logger.debug("检查设置")
    is_set_up = ImageService.touch(Onmyoji.explore_SZ)
    if is_set_up:
        logger.debug("检查轮换数量")
        num_full = OcrService.get_word(Onmyoji.explore_DQLHSL, lang='chi_sim')
        if num_full is not None and num_full == '50':
            logger.debug("轮换数量已满")
        elif num_full is not None and num_full != '50':
            logger.debug("点击左下全部")
            ImageService.touch(Onmyoji.explore_ZXQB)
            logger.debug("点击左下N卡")
            ImageService.touch(Onmyoji.explore_ZXNK)
            logger.debug("点击候补式神")
            ImageService.touch(Onmyoji.explore_HBSS)
            logger.debug("检查轮换数量,5次")
            for i_full in range(10):
                logger.debug("检查轮换数量")
                num_full = OcrService.get_word(Onmyoji.explore_DQLHSL, lang='chi_sim')
                if num_full is not None and num_full == '50':
                    logger.debug("轮换数量已满")
                    break
                else:
                    logger.debug("轮换数量不满50,检查一级N卡")
                    is_ration = ImageService.find_all(Onmyoji.explore_YJNK)
                    if is_ration:
                        logger.debug("获取一级N卡纵坐标最大的坐标")
                        result = max(is_ration, key=lambda x: x['result'][1])['result']
                        logger.debug("长按一级N卡")
                        ImageService.touch_coordinate(result, duration=2)
                    else:
                        logger.debug("没有符合条件的N卡，检查滚轮")
                        is_roller = ImageService.exists(Onmyoji.explore_LHGL, cvstrategy=Cvstrategy.default)
                        if is_roller:
                            logger.debug("滑动滚轮")
                            ImageService.swipe(is_roller, (is_roller[0] + is_roller[0] * 0.1, is_roller[1]))

        else:
            logger.debug("没找到轮换数量")
    logger.debug("轮换确定")
    ImageService.touch(Onmyoji.explore_LHQD)
    ImageService.touch(Onmyoji.comm_FH_YSJBDHSCH)


def submit_emaki():
    logger.debug("首页召唤")
    logger.debug("右上绘卷")
    logger.debug("点击左下角，排除干扰")
    logger.debug("选择图四")
    logger.debug("拉满大碎片")
    logger.debug("拉满中碎片")
    logger.debug("拉满小碎片")
    logger.debug("捐赠")
    logger.debug("领取奖励")
    logger.debug("返回首页")
