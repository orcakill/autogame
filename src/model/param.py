# 项目
class ProjectParam:
    def __int__(self, project_name: str, project_user: str, project_num: int, project_wait_start_time: int,
                project_wait_end_time: int):
        # 项目名称
        self.project_name = project_name
        # 项目账号
        self.project_user = project_user
        # 项目执行次数
        self.project_num = project_num
        #  项目执行前等待时间
        self.project_wait_start_time = project_wait_start_time
        # 项目执行后等待时间
        self.project_wait_end_time = project_wait_end_time


# 项目组
class ProjectsParam:
    def __init__(self, projects_name: str, projects_round: int, project_params: []):
        # 项目组名称
        self.projects_name = projects_name
        # 执行轮次
        self.projects_round = projects_round
        # 项目信息
        self.project_params = project_params
