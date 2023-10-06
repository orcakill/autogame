"""
# @Time: 2023年10月01日17:34
# @Author: orcakill
# @File: impl_blog.py
# @Description: 微博内容获取
"""
import requests


def get_blog(size: int = 10):
    # 设置API密钥
    client_id = 'your_client_id'  # 替换为你的应用的API Key
    client_secret = 'your_client_secret'  # 替换为你的应用的API Secret
    access_token = 'your_access_token'  # 替换为你的应用的访问令牌

    # 设置API请求的URL和参数
    url = 'https://api.weibo.com/2/statuses/user_timeline.json'
    params = {
        'access_token': access_token,
        'uid': 'user_id',  # 替换为你要获取微博的用户ID
        'count': 10  # 获取最近十条微博
    }

    # 发送API请求
    response = requests.get(url, params=params)

    # 解析API响应并打印微博内容
    if response.status_code == 200:
        data = response.json()
        for status in data['statuses']:
            print(status['text'])
    else:
        print('请求失败')
