# @Time: 2023年12月21日 19:13
# @Author: orcakill
# @File: impl_super.py
# @Description: 超鬼王

import time

from src.dao.mapper import Mapper
from src.model.models import GameProjectsRelation, GameProjectLog, GameAccount, GameProject, GameDevices
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.utils.my_logger import logger
from src.utils.utils_time import UtilsTime


def super_ghost(game_task: []):
	"""
        超鬼王，自动打难超鬼王以下
        :param game_task:  任务信息
        :return:
        """
	# 活动变量
	super_SFHY = r"活动\20231221\超鬼王\上方好友"
	super_RK1 = r"活动\20231221\超鬼王\入口1"
	super_RK2 = r"活动\20231221\超鬼王\入口2"
	super_ZB = r"活动\20231221\超鬼王\准备"
	super_HC = r"活动\20231221\超鬼王\喝茶"
	super_HCTX = r"活动\20231221\超鬼王\喝茶提醒"
	super_ZDSB = r"活动\20231221\超鬼王\战斗失败"
	super_ZDSL = r"活动\20231221\超鬼王\战斗胜利"
	super_TZ = r"活动\20231221\超鬼王\挑战"
	super_SSGW = r"活动\20231221\超鬼王\搜索鬼王"
	super_PT = r"活动\20231221\超鬼王\普通"
	super_QL = r"活动\20231221\超鬼王\强力"
	super_MBHY = r"活动\20231221\超鬼王\目标好友"
	super_JSZ = r"活动\20231221\超鬼王\结算中"
	super_ZD = r"活动\20231221\超鬼王\自动"
	super_HDJL = r"活动\20231221\超鬼王\获得奖励"
	super_ZSJF = r"活动\20231221\超鬼王\赠送积分"
	super_ZSJFQR = r"活动\20231221\超鬼王\赠送积分确认"
	super_CGWSY = r"活动\20231221\超鬼王\超鬼王首页"
	super_YQ = r"活动\20231221\超鬼王\邀请"
	super_ND_Z = r"活动\20231221\超鬼王\难度\中"
	super_ND_Y = r"活动\20231221\超鬼王\难度\易"
	super_ND_J = r"活动\20231221\超鬼王\难度\极"
	super_ND_N = r"活动\20231221\超鬼王\难度\难"
	super_ND_G = r"活动\20231221\超鬼王\难度\高"
	super_JJ = r"活动\20231221\超鬼王\集结"
	# super_BJSS = r"活动\20231221\超鬼王\标记式神"
	# 开始时间
	time_start = time.time()
	# 项目信息
	game_projects_relation, game_account, game_project, game_devices = (
		GameProjectsRelation(game_task[1]), GameAccount(game_task[2]), GameProject(game_task[3]),
		GameDevices(game_task[4]))
	# 战斗次数
	fight_time = game_projects_relation.project_num_times or 200
	# 难度列表
	difficulty_list = [super_ND_Y, super_ND_Z, super_ND_G, super_ND_N, super_ND_J]
	logger.debug("1.战斗前准备")
	is_home = False
	for i_come in range(3):
		logger.debug("拒接协战")
		ComplexService.refuse_reward()
		logger.debug("入口1")
		ImageService.touch(super_RK1)
		time.sleep(5)
		logger.debug("入口2")
		ImageService.touch(super_RK2, timeouts=30)
		logger.debug("检查赠送积分")
		is_gifts = ImageService.exists(super_ZSJF)
		if is_gifts:
			logger.debug("确认")
			ImageService.touch(super_ZSJFQR)
			logger.debug("获得奖励")
			ComplexService.get_reward(super_HDJL)
		is_home = ImageService.exists(super_CGWSY)
		if is_home:
			logger.debug("确定进入超鬼王首页")
			break
	if is_home:
		for i in range(fight_time):
			logger.debug("检查是否鬼王首页，是否喝茶")
			is_home = ImageService.exists(super_CGWSY)
			is_tea = ImageService.exists(super_HCTX)
			if is_home and not is_tea:
				is_add = ImageService.exists(super_JSZ)
				if is_add:
					logger.debug("结算中，等待10s")
					time.sleep(10)
				logger.debug("搜索鬼王")
				ImageService.touch(super_SSGW)
				logger.debug("检查鬼王难度，发现难和极中断")
				is_difficulty = ComplexService.check_list(difficulty_list)
				logger.debug("当前鬼王难度{}", is_difficulty)
				if is_difficulty in [super_ND_J, super_ND_N, super_ND_G]:
					time.sleep(3)
					logger.debug("点击集结")
					is_gathering = ImageService.touch(super_JJ)
					if is_gathering:
						logger.debug("获取上方好友坐标")
						pos_friend = ImageService.exists(super_SFHY)
						if pos_friend:
							logger.debug("好友坐标{}", pos_friend)
							pos1 = (pos_friend[0], pos_friend[1] * 2)
							pos2 = (pos_friend[0], pos_friend[1] * 3)
							for i_move in range(20):
								logger.debug("检查目标好友,{}次", i_move + 1)
								is_target = ImageService.touch(super_MBHY)
								if is_target:
									logger.debug("邀请目标好友")
									ImageService.touch(super_YQ)
									break
								ImageService.swipe(pos2, pos1)
							logger.debug("退出集结")
							ComplexService.get_reward(super_SFHY)
					else:
						logger.debug("无集结,等待1分钟")
						time.sleep(60)
					logger.debug("集结好友战斗中，等待1分钟")
					time.sleep(60)
				elif is_difficulty is not None:
					logger.debug("点击普通")
					ImageService.touch(super_PT)
					if is_difficulty in [super_ND_G]:
						logger.debug("点击强力")
						ImageService.touch(super_QL)
					logger.debug("挑战")
					ImageService.touch(super_TZ)
					time.sleep(5)
					logger.debug("准备")
					ImageService.touch(super_ZB)
					ImageService.touch(super_ZB)
					logger.debug("检查是否自动战斗")
					is_auto = ImageService.exists(super_ZD, timeouts=10)
					if is_auto:
						# logger.debug("标记式神")
						# ImageService.touch(super_BJSS)
						logger.debug("自动战斗中，等待结果")
						ComplexService.fight_end(super_ZDSL, super_ZDSB, super_ZDSB, super_ZDSL, None, None, 60 * 5, 2)
						is_add = ImageService.exists(super_JSZ)
						if is_add:
							logger.debug("结算中，等待10s")
							time.sleep(10)
			else:
				logger.debug("处理异常情况")
				ComplexService.refuse_reward()
				logger.debug("重新准备")
				ImageService.touch(super_ZB)
				logger.debug("战斗胜利")
				ImageService.touch(super_ZDSL)
				logger.debug("战斗失败")
				ImageService.touch(super_ZDSB)
				logger.debug("检查是否喝茶")
				is_tea = ImageService.exists(super_HCTX)
				if is_tea:
					logger.debug("喝茶")
					ImageService.touch(super_HC)
	logger.debug("4.战斗结算")
	# 结束时间
	time_end = time.time()
	# 总用时
	time_all = time_end - time_start
	# 记录项目执行结果
	game_project_log = GameProjectLog(project_id=game_project.id, role_id=game_account.id, devices_id=game_devices.id,
	                                  result='活动-超鬼王完成', cost_time=int(time_all))
	Mapper.save_game_project_log(game_project_log)
	logger.debug("本轮活动-超鬼王十总用时{}", UtilsTime.convert_seconds(time_all))
