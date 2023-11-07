# @Time: 2023年09月06日 11:50
# @Author: orcakill
# @File: utils_time.py
# @Description: 时间工具类
from datetime import datetime


class UtilsTime:
    @staticmethod
    def convert_seconds(seconds):
        if seconds < 60:
            return f"{round(seconds)}秒"
        elif seconds < 3600:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{round(minutes)}分钟 {round(seconds)}秒"
        elif seconds < 86400:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = (seconds % 3600) % 60
            return f"{round(hours)}小时 {round(minutes)}分钟 {round(seconds)}秒"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            minutes = ((seconds % 86400) % 3600) // 60
            seconds = ((seconds % 86400) % 3600) % 60
            return f"{round(days)}天 {round(hours)}小时 {round(minutes)}分钟 {round(seconds)}秒"

    @staticmethod
    def get_day_str():
        # 获取当前日期
        current_date = datetime.now().date()
        # 将日期转换为字符串类型
        date_string = current_date.strftime('%Y-%m-%d')
        return date_string


if __name__ == '__main__':
    print(UtilsTime.convert_seconds(30))
    print(UtilsTime.get_day_str())
