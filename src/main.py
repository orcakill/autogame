import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.service.complex_service import ComplexService
from src.controller.onmyoji_controller import OnmyojiController
from src.dao.mapper_extend import MapperExtend
from src.model.models import GameProjects, GameProject
from src.service.windows_service import WindowsService
from src.utils.my_logger import my_logger as logger
from src.utils.utils_mail import UtilsMail

if __name__ == '__main__':
    WindowsService.limit_cpu_percentage(30)
    game_id = ''
    project_num = ''
    logger.info("脚本启动")
    logger.info("设备: 0 云手机001 1 夜神模拟器 2荣耀平板 3小米手机 4 云手机002")
    projects = MapperExtend.select_game_projects("", "")
    project = MapperExtend.select_game_project("", "")
    logger.info("可执行项目组:")
    for i in range(len(projects)):
        game_projects = GameProjects(projects[i])
        logger.info("   {}:{}", game_projects.projects_num, game_projects.projects_name)
    logger.info("可执行项目:")
    for i in range(len(project)):
        game_project = GameProject(project[i])
        logger.info("   {}:{}", game_project.project_num, game_project.project_name)
    logger.info("**************")
    game_device = input("请输入一个设备编号：")
    game_num = input("请输入一个项目组编号：")
    if not game_num:
        logger.debug("无项目组，按项目和账号执行")
        project_num = input("请输入一组项目编号：")
        game_id = input("请输入一组账号：")
    game_round = input("请输入一个项目组轮次：")
    game_relation_num = input("请输入一个项目组开始执行编号：")
    # 0 每个节点都发送邮件 1 进程结束后发送邮件  2不发送邮件
    game_is_email = "1"
    logger.info("**************")
    logger.info("脚本类型{},脚本轮次 {},连接设备{}", game_num, game_round, game_device)
    logger.info("**************")
    logger.info("执行任务")
    ComplexService.auto_setup(game_device)
    if game_num:
        OnmyojiController.create_execute_tasks(game_device, game_id, projects_num=game_num, game_round=game_round,
                                               relation_num=game_relation_num)
    else:
        OnmyojiController.create_execute_tasks(game_device, game_id, project_num=project_num, game_round=game_round,
                                               relation_num=game_relation_num)
    if game_is_email == '1':
        logger.info("发送邮件")
        UtilsMail.send_email("阴阳师脚本", "结束", "项目组执行结束")
