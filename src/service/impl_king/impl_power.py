# @Time: 2025年06月25日 11:59
# @Author: orcakill
# @File: impl_power.py
# @Description: 通过王者营地的克制关系，筛选出对抗路需要必练的英雄
import json
import re
import time

import pandas as pd
import requests

from src.model.enum import Onmyoji
from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.impl_image_service.impl_ocr import ImplOcr
from src.service.ocr_service import OcrService
from src.utils.my_logger import logger


class ImplPower:
    @staticmethod
    def get_honor_of_kings_heroes():
        """
        获取王者荣耀全英雄列表
        :return: 英雄名字列表
        """
        api_url = 'https://pvp.qq.com/web201605/js/herolist.json'
        try:
            # 发送HTTP请求
            response = requests.get(api_url, timeout=10)
            response.encoding = 'utf-8'  # 强制使用UTF-8编码

            if response.status_code == 200:
                # 解析JSON数据
                heroes_data = json.loads(response.text)
                return [hero['cname'] for hero in heroes_data]
            return []
        except Exception as e:
            print(f"英雄列表请求失败: {e}")
            return []

    @staticmethod
    def get_restraint_factor(results, exclude_name, heroes_list):
        """
        筛选关联结果
        :param results: OCR识别结果
        :param exclude_name: 需要排除的英雄名
        :param heroes_list: 英雄列表
        :return: 筛选后的结果 [[英雄名, 关联数据], ...]
        """
        filtered_results = []
        # 严格匹配纯小数（排除包含汉字、百分号和其他符号）
        decimal_pattern = re.compile(r'^\d+\.\d+$')

        # 遍历所有英雄
        for hero in heroes_list:
            if hero == exclude_name:
                continue

            # 遍历识别结果
            for i in range(len(results)):
                # 检查英雄名是否在结果中
                if hero in results[i][0]:
                    # 向后查找第一个有效数值
                    for j in range(i + 1, len(results)):
                        # 清洗数据：去除空格和特殊符号
                        clean_str = results[j][0].strip().replace('%', '')
                        # 严格匹配纯小数格式
                        if decimal_pattern.match(clean_str):
                            filtered_results.append([hero, clean_str])
                            break
                    break  # 找到后跳出当前英雄的循环
        return filtered_results

    @staticmethod
    def deal_data():
        # 设置循环的分路
        shunt = '对抗路'
        # 连接设备
        ComplexService.auto_setup("1")
        # 获取全部英雄列表
        kings_heroes = ImplPower.get_honor_of_kings_heroes()
        # 更多内容标志
        is_connect_flag = False
        # 监测结果
        check_heros = []
        check_result = []

        while not is_connect_flag:
            # 获取当前设备英雄列表
            heros_axis_list = ImplOcr.ocr_list(kings_heroes)
            heros_axis_list_bak = heros_axis_list.copy()
            # 排除掉已处理的英雄
            for hero in heros_axis_list:
                if hero[0] in check_heros:
                    heros_axis_list.remove(hero)
            #  如果已全部处理，判断是否有更多内容，没有则执行下滑，有则结束循环
            if len(heros_axis_list) == 0:
                no_content = ImplOcr.ocr_list("没有更多内容")
                if len(no_content) != 0:
                    # 如果全部已处理，且有更多内容，跳出循环
                    is_connect_flag = True
                    break
                else:
                    # 如果全部已处理，且没有更多内容，执行下滑
                    ImageService.swipe(heros_axis_list_bak[-1][1], heros_axis_list_bak[0][1], 2)
            # 有未处理的英雄
            if len(heros_axis_list) > 0:
                # 点击第一个英雄坐标
                logger.info('点击英雄{}', heros_axis_list[0][0])
                ImageService.touch_coordinate(heros_axis_list[0][1])
                time.sleep(5)
                # 点击克制
                logger.info('点击克制')
                ImplOcr.ocr_touch(['克制'], ['被克制'])
                # 获取克制关系
                restraint_word = ImplOcr.ocr_list([])
                restraint_relationship = ImplPower.get_restraint_factor(restraint_word, heros_axis_list[0][0],
                                                                        kings_heroes)
                for relationship in restraint_relationship:
                    # 对抗路  东皇太一 克制  姬小满  4.81
                    check_result.append([shunt, heros_axis_list[0][0], '克制', relationship[0], relationship[1]])
                # 点击被克制
                logger.info('点击被克制')
                ImplOcr.ocr_touch(['被克制'], ['克制'])
                time.sleep(5)
                # 获取被克制关系
                restrained_word = ImplOcr.ocr_list([])
                restrained_relationship = ImplPower.get_restraint_factor(restrained_word, heros_axis_list[0][0],
                                                                         kings_heroes)
                for relationship in restrained_relationship:
                    # 对抗路  东皇太一  被克制  姬小满  4.81
                    check_result.append([shunt, heros_axis_list[0][0], '被克制', relationship[0], relationship[1]])
                # 点击返回英雄列表
                logger.info('点击返回')
                ImageService.keyevent_back()
                time.sleep(5)
            break
        # 将克制关系和被克制关系处理到excel中
        # 新增Excel导出部分（添加在while循环之后）
        if check_result:
            df = pd.DataFrame(check_result, columns=['分路', '英雄', '关系', '关联英雄', '系数'])
            df.to_excel(shunt + '.xlsx', index=False)
            print(f"已生成Excel文件，记录数：{len(df)}")
        else:
            print("未找到有效克制关系数据")


if __name__ == '__main__':
    ImplPower.deal_data()
