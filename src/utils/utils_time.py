# @Time: 2023年09月06日 11:50
# @Author: orcakill
# @File: utils_time.py
# @Description: 时间工具类

class UtilsTime():
    @staticmethod
    def convert_seconds(seconds):
        if seconds < 60:
            return f"{seconds}秒"
        elif seconds < 3600:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes}分钟 {seconds}秒"
        elif seconds < 86400:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = (seconds % 3600) % 60
            return f"{hours}小时 {minutes}分钟 {seconds}秒"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            minutes = ((seconds % 86400) % 3600) // 60
            seconds = ((seconds % 86400) % 3600) % 60
            return f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"


if __name__ == '__main__':
    print(UtilsTime.convert_seconds(30))

