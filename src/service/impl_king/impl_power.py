# @Time: 2025年06月25日 11:59
# @Author: orcakill
# @File: impl_power.py
# @Description: 通过王者营地的克制关系，筛选出对抗路需要必练的英雄
import json

import pandas as pd
import requests

from src.service.airtest_service import AirtestService
from src.service.complex_service import ComplexService
from src.service.image_service import ImageService
from src.service.ocr_service import OcrService


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
        # 遍历所有英雄
        for hero in heroes_list:
            # 跳过排除的英雄
            if hero == exclude_name:
                continue

            # 遍历识别结果
            for i in range(len(results) - 1):  # 防止越界
                # 检查英雄名是否在结果中
                if hero in results[i][0]:
                    filtered_results.append([hero, results[i + 1][0]])
        return filtered_results


if __name__ == '__main__':
    # 设置循环的分路
    shunt = '对抗路'
    # 连接设备
    ComplexService.auto_setup("1")
    # 获取全部英雄列表
    kings_heroes = ImplPower.get_honor_of_kings_heroes()
    # 更多内容标志
    is_connect_flag = False
    # 监测结果
    check_result = {}
    while not is_connect_flag:
        # 获取当前设备英雄列表,进行屏幕截图
        screen = AirtestService.snapshot()
        # 基于屏幕截图和英雄名称获取列表坐标
        heros_axis_list = OcrService.ocr_paddle_list(screen, kings_heroes)
        # 点击第一个英雄坐标
        ImageService.touch_coordinate(heros_axis_list[0])
        # 点击克制
        screen1 = AirtestService.snapshot()
        restraint_coordinate = OcrService.ocr_paddle(screen1, '克制')
        ImageService.touch_coordinate(heros_axis_list[restraint_coordinate])
        # 获取克制关系
        # 数据加工，组织成 对抗路  东皇太一  克制  姬小满   5.68
        # 点击被克制
        # 获取被克制关系
        # 点击返回英雄列表，进入下一个英雄
        # 列表英雄循环完成，点击下滑
        # 识别到屋更多内容，结束循环
        # 将克制关系和被克制关系处理到excel中
        a = 1
