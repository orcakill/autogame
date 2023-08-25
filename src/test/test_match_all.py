"""
# @Time: 2023年08月25日22:08
# @Author: orcakill
# @File: test_match_all.py
# @Description: TODO
"""
from airtest.core.api import *
from airtest.core.cv import Template

from src.service.image_service import ImageService

image_service = ImageService()

if __name__ == '__main__':
    # 设置设备连接
    image_service.auto_setup("0")
    # 定义黄色星星的模板
    yellow_star_template = Template("D:/a.png", threshold=0.7)

    # 在截图中查找黄色星星的数量
    screenshot = image_service.snapshot("测试")
    result = screenshot.match_all_in(yellow_star_template)

    # 输出黄色星星的数量
    print("黄色星星的数量：", len(result))
