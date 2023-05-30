from src.controller.onmyoji_controller import task
from utils.my_logger import my_logger as logger

if __name__ == '__main__':
    logger.info("脚本启动")
    logger.info()
    game_type = input("请输入一个脚本类型：")
    game_round = input("请输入一个脚本轮次：")
    # 0 每个节点都发送邮件 1 进程结束后发送邮件  2不发送邮件
    game_is_email = "0"
    logger.info("脚本类型 {},脚本轮次 {}", game_type, game_round)
    # 执行项目组、每个节点整理邮件报告
    task(game_type, game_round, game_is_email)
