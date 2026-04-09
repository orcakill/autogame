# @Time: 2026年04月09日 10:26
# @Author: orcakill
# @File: impl_house_optimized.py
# @Description: 优化后的结界卡寄养逻辑
import time
from src.service.image_service import ImageService
from src.service.complex_service import ComplexService
from src.model.enum import Onmyoji
from src.utils.my_logger import logger


class ImplHouseOptimized:
    """
    优化后的结界卡寄养实现
    采用两阶段逻辑：
    1. 第一遍：统计所有结界卡情况
    2. 第二遍：直接定位到最优结界卡
    """
    
    @staticmethod
    def get_optimal_card():
        """
        优化后的获取最优结界卡函数
        两阶段逻辑：统计 -> 执行
        :return: 最优结界卡位置或None
        """
        logger.debug("开始优化版结界卡寄养逻辑")
        
        # 第一阶段：统计所有结界卡情况
        card_statistics = ImplHouseOptimized._collect_card_statistics()
        
        if not card_statistics:
            logger.debug("统计阶段失败，退出寄养")
            return None
        
        # 分析最优结界卡
        best_card_info = ImplHouseOptimized._analyze_best_card(card_statistics)
        
        if not best_card_info:
            logger.debug("未找到合适的结界卡，退出寄养")
            return None
        
        best_card, best_position = best_card_info
        logger.debug(f"最优结界卡：{best_card}，位置：{best_position}")
        
        # 第二阶段：定位并执行寄养
        result = ImplHouseOptimized._locate_and_foster(best_card, best_position)
        
        if result:
            logger.debug("寄养成功")
            return best_card
        else:
            logger.debug("寄养失败，退出")
            return None
    
    @staticmethod
    def _collect_card_statistics():
        """
        第一阶段：统计所有结界卡情况
        :return: 结界卡统计信息
        """
        logger.debug("开始统计结界卡情况")
        
        # 初始化统计结构
        card_statistics = {
            'six_star': [],  # 六星结界卡列表 [(card_type, position), ...]
            'five_star': [],  # 五星结界卡列表
            'four_star': [],  # 四星结界卡列表
            'all_cards': []    # 所有结界卡列表
        }
        
        # 寄养开始时间
        time_start = time.time()
        
        # 获取好友和跨区坐标
        coordinate_friend = ()
        coordinate_region = ()
        
        for i_sign in range(3):
            logger.debug("寄养--点击可寄养标志")
            ImageService.touch(Onmyoji.foster_KJYBZ, timeouts=10, wait=5)
            logger.debug("寄养-获取上方好友坐标")
            coordinate_friend = ImageService.exists(Onmyoji.foster_SFHY)
            logger.debug("寄养-获取上方跨区坐标")
            coordinate_region = ImageService.exists(Onmyoji.foster_SFKQ)
            if coordinate_friend and coordinate_region:
                logger.debug("找到上方好友和上方跨区")
                break
            else:
                logger.debug("退出好友寄养列表")
                ComplexService.get_reward(Onmyoji.foster_SFHY)
        
        if not (coordinate_friend and coordinate_region):
            logger.debug("未获取到上方好友和上方跨区")
            return None
        
        # 计算坐标间距
        coordinate_difference = 0.8228571428571428 * (coordinate_region[0] - coordinate_friend[0])
        coordinate_difference1 = 0.8902849002849003 * (coordinate_region[0] - coordinate_friend[0])
        
        # 计算好友位置
        coordinate_friend1 = (coordinate_region[0], coordinate_region[1] + coordinate_difference)
        coordinate_friend2 = (
            coordinate_region[0], coordinate_region[1] + coordinate_difference + 1 * coordinate_difference1)
        coordinate_friend3 = (
            coordinate_region[0], coordinate_region[1] + coordinate_difference + 2 * coordinate_difference1)
        coordinate_friend4 = (
            coordinate_region[0], coordinate_region[1] + coordinate_difference + 3 * coordinate_difference1)
        
        # 遍历好友
        for i_friends in range(10):
            logger.debug(f"统计第{i_friends + 1}轮好友结界卡")
            
            if time.time() - time_start > 20 * 60:
                logger.debug("统计执行时间超20分钟，停止统计")
                break
            
            # 拒接协战
            ComplexService.refuse_reward()
            
            # 点击四个好友位置
            friend_positions = [coordinate_friend1, coordinate_friend2, coordinate_friend3, coordinate_friend4]
            for pos in friend_positions:
                ImageService.touch_coordinate(pos, wait=0.5)
            
            # 检查左侧结界卡
            card_info = ImplHouseOptimized._check_current_card()
            if card_info:
                card_type, position = card_info
                # 分类结界卡
                if card_type in [Onmyoji.foster_JJK_LXTG, Onmyoji.foster_JJK_LXDY]:
                    card_statistics['six_star'].append((card_type, position))
                    card_statistics['all_cards'].append((card_type, position))
                elif card_type in [Onmyoji.foster_JJK_WXTG, Onmyoji.foster_JJK_WXDY]:
                    card_statistics['five_star'].append((card_type, position))
                    card_statistics['all_cards'].append((card_type, position))
                elif card_type in [Onmyoji.foster_JJK_SXTG, Onmyoji.foster_JJK_SXTG1, 
                                 Onmyoji.foster_JJK_SXDY, Onmyoji.foster_JJK_SXDY1]:
                    card_statistics['four_star'].append((card_type, position))
                    card_statistics['all_cards'].append((card_type, position))
            
            # 检查是否未放置
            is_unplaced = ImageService.exists(Onmyoji.foster_JJK_WFZ)
            if is_unplaced:
                logger.debug("发现未放置结界卡，中断当前轮次")
                ComplexService.get_reward(Onmyoji.foster_SFHY)
                break
            
            if i_friends == 9:
                logger.debug("超出40个好友，停止统计")
                ComplexService.get_reward(Onmyoji.foster_SFHY)
                break
            
            # 向下滑动
            logger.debug("向下滑动4位好友")
            ComplexService.refuse_reward()
            ImageService.swipe(coordinate_friend4, coordinate_friend1, 2)
        
        logger.debug(f"统计完成：六星{len(card_statistics['six_star'])}张, 五星{len(card_statistics['five_star'])}张, 四星{len(card_statistics['four_star'])}张")
        return card_statistics
    
    @staticmethod
    def _check_current_card():
        """
        检查当前好友的结界卡类型
        :return: (card_type, position) 或 None
        """
        # 检查左侧结界卡
        target_cards = [
            Onmyoji.foster_ZCJJK_LXTG,  # 六星太鼓
            Onmyoji.foster_ZCJJK_LXDY,  # 六星斗鱼
            Onmyoji.foster_ZCJJK_WXTG,  # 五星太鼓
            Onmyoji.foster_ZCJJK_WXDY,  # 五星斗鱼
            Onmyoji.foster_ZCJJK_SXTG,  # 四星太鼓
            Onmyoji.foster_ZCJJK_SXTG1, # 四星太鼓1
            Onmyoji.foster_ZCJJK_SXDY,  # 四星斗鱼
            Onmyoji.foster_ZCJJK_SXDY1  # 四星斗鱼1
        ]
        
        for target_card in target_cards:
            result = ImplHouseOptimized._get_card_left_type(target_card)
            if result and result[0] == target_card:
                return target_card, result[1]
        
        return None
    
    @staticmethod
    def _get_card_left_type(target_card: str):
        """
        获取当前结界卡,直接判断左侧是否有目标结界卡
        :param target_card: 目标结界卡
        :return: [target_card, position, confidence] 或 None
        """
        def check_image_confidence(image, threshold, rgb):
            if image:
                if image == Onmyoji.foster_JJK_WFZ:
                    result = ImageService.cv_match(image, threshold=threshold, rgb=rgb, x1=0.5)
                else:
                    result = ImageService.cv_match(image, threshold=threshold, rgb=rgb, x2=0.5)
                return result
            return 0
        
        card_types = [target_card, Onmyoji.foster_JJK_WFZ]
        
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_image_confidence, image_path, 0.6, False) for image_path in card_types]
        results = [future.result() for future in futures]
        
        if results[0]:
            logger.debug(f"检查结果：{target_card}, 相似度：{results[0]['confidence']}")
            return [target_card, results[0]['result'], results[0]['confidence']]
        elif results[1]:
            logger.debug(f"检查结果：{Onmyoji.foster_JJK_WFZ}")
            return [Onmyoji.foster_JJK_WFZ, None, 0]
        
        logger.debug("检查结果：其他情况")
        return None
    
    @staticmethod
    def _analyze_best_card(card_statistics):
        """
        分析最优结界卡
        优先级：六星太鼓 > 六星斗鱼 > 五星太鼓 > 五星斗鱼 > 四星太鼓 > 四星斗鱼
        :param card_statistics: 结界卡统计信息
        :return: (best_card, best_position) 或 None
        """
        logger.debug("开始分析最优结界卡")
        
        # 定义优先级顺序
        priority_order = [
            Onmyoji.foster_JJK_LXTG,  # 六星太鼓（最高）
            Onmyoji.foster_JJK_LXDY,  # 六星斗鱼
            Onmyoji.foster_JJK_WXTG,  # 五星太鼓
            Onmyoji.foster_JJK_WXDY,  # 五星斗鱼
            Onmyoji.foster_JJK_SXTG,  # 四星太鼓
            Onmyoji.foster_JJK_SXTG1, # 四星太鼓1
            Onmyoji.foster_JJK_SXDY,  # 四星斗鱼
            Onmyoji.foster_JJK_SXDY1  # 四星斗鱼1（最低）
        ]
        
        # 合并所有结界卡
        all_cards = card_statistics['all_cards']
        
        if not all_cards:
            logger.debug("无结界卡可分析")
            return None
        
        # 按优先级排序
        sorted_cards = []
        for priority_card in priority_order:
            for card in all_cards:
                if card[0] == priority_card:
                    sorted_cards.append(card)
        
        if sorted_cards:
            best_card, best_position = sorted_cards[0]
            logger.debug(f"最优结界卡：{best_card}")
            return best_card, best_position
        
        return None
    
    @staticmethod
    def _locate_and_foster(target_card, target_position):
        """
        第二阶段：定位并执行寄养
        :param target_card: 目标结界卡
        :param target_position: 目标位置
        :return: 是否成功
        """
        logger.debug(f"开始定位并寄养：{target_card}")
        
        try:
            # 点击目标位置
            logger.debug(f"点击目标位置：{target_position}")
            ImageService.touch_coordinate(target_position)
            
            # 验证结界卡类型
            logger.debug("验证结界卡类型")
            card_type = ImplHouseOptimized._get_card_type_word(target_card, Onmyoji.foster_JJK_GYWZ, 0)
            
            if card_type == target_card:
                logger.debug("结界卡类型验证成功")
                return True
            else:
                logger.debug(f"结界卡类型验证失败，期望：{target_card}，实际：{card_type}")
                return False
                
        except Exception as e:
            logger.exception(f"定位寄养异常：{e}")
            return False
    
    @staticmethod
    def _get_card_type_word(target_type: str, target_word, not_placed: int = 0):
        """
        获取文字识别结界卡类型
        :param target_type: 目标类型
        :param target_word: 目标文字
        :param not_placed: 是否检查未放置
        :return: 结界卡类型或None
        """
        from src.service.ocr_service import OcrService
        
        logger.debug("获取文字")
        result = OcrService.get_word(target_word)
        
        if result:
            if result in ['67', '76'] and target_type in [Onmyoji.foster_JJK_LXTG, Onmyoji.foster_JJK_WXTG]:
                logger.debug(f"检查结果：{target_type}")
                return target_type
            if result in ['59', '67'] and target_type in [Onmyoji.foster_JJK_WXTG]:
                logger.debug(f"检查结果：{target_type}")
                return target_type
            if result in ['50'] and target_type in [Onmyoji.foster_JJK_SXTG1]:
                logger.debug(f"检查结果：{target_type}")
                return target_type
            if result in ['42', '50'] and target_type in [Onmyoji.foster_JJK_SXTG1, Onmyoji.foster_JJK_SXTG]:
                logger.debug(f"检查结果：{target_type}")
                return target_type
        
        if not_placed == 1:
            is_placed = ImageService.exists(Onmyoji.foster_JJK_WFZ)
            if is_placed:
                logger.debug(f"检查结果：{Onmyoji.foster_JJK_WFZ}")
                return Onmyoji.foster_JJK_WFZ
        
        logger.debug("检查结果：其他情况")
        return None
