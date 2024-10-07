# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GameAccount(Base):
    __tablename__ = "game_account"

    id = Column(String(40), primary_key=True, info='ID')
    account_num = Column(Integer, info='账号序号')
    account_type = Column(String(40), info='账号类型')
    account_name = Column(String(40), info='账号名称')
    account_password = Column(String(40), info='账号密码')
    role_region = Column(String(40), info='角色服务器')
    role_name = Column(String(40), info='角色名称')
    role_class = Column(String(40), info='角色等级')
    game_package = Column(Integer, info='游戏包名')
    game_acivity = Column(Integer, info='游戏活动名')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"account_num= {self.account_num}," \
               f"account_type= {self.account_type}," \
               f"account_name= {self.account_name}," \
               f"account_password= {self.account_password}," \
               f"role_region= {self.role_region}," \
               f"role_name= {self.role_name}," \
               f"role_class= {self.role_class}," \
               f"game_package= {self.game_package}," \
               f"game_acivity= {self.game_acivity}"

    def __init__(self, game_account: () = None, **kwargs):
        if game_account is None:
            self.id = kwargs.get('id')
            self.account_num = kwargs.get('account_num')
            self.account_type = kwargs.get('account_type')
            self.account_name = kwargs.get('account_name')
            self.account_password = kwargs.get('account_password')
            self.role_region = kwargs.get('role_region')
            self.role_name = kwargs.get('role_name')
            self.role_class = kwargs.get('role_class')
            self.game_package = kwargs.get('game_package')
            self.game_acivity = kwargs.get('game_acivity')
        else:
            super().__init__(**kwargs)
            self.id = game_account.id
            self.account_num = game_account.account_num
            self.account_type = game_account.account_type
            self.account_name = game_account.account_name
            self.account_password = game_account.account_password
            self.role_region = game_account.role_region
            self.role_name = game_account.role_name
            self.role_class = game_account.role_class
            self.game_package = game_account.game_package
            self.game_acivity = game_account.game_acivity


class GameAccounts(Base):
    __tablename__ = "game_accounts"

    id = Column(String(40), primary_key=True, info='账号组标识')
    accounts_num = Column(Integer, info='账号组序号')
    accounts_name = Column(String(40), info='账号组名称')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"accounts_num= {self.accounts_num}," \
               f"accounts_name= {self.accounts_name}"

    def __init__(self, game_accounts: () = None, **kwargs):
        if game_accounts is None:
            self.id = kwargs.get('id')
            self.accounts_num = kwargs.get('accounts_num')
            self.accounts_name = kwargs.get('accounts_name')
        else:
            super().__init__(**kwargs)
            self.id = game_accounts.id
            self.accounts_num = game_accounts.accounts_num
            self.accounts_name = game_accounts.accounts_name


class GameAccountsRelation(Base):
    __tablename__ = "game_accounts_relation"

    id = Column(String(40), primary_key=True, info='账号组关系标识')
    relation_num = Column(Integer, info='账号组关系序号')
    acounts_id = Column(String(40), info='账号组标识')
    account_id = Column(String(40), info='账号标识')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"relation_num= {self.relation_num}," \
               f"acounts_id= {self.acounts_id}," \
               f"account_id= {self.account_id}"

    def __init__(self, game_accounts_relation: () = None, **kwargs):
        if game_accounts_relation is None:
            self.id = kwargs.get('id')
            self.relation_num = kwargs.get('relation_num')
            self.acounts_id = kwargs.get('acounts_id')
            self.account_id = kwargs.get('account_id')
        else:
            super().__init__(**kwargs)
            self.id = game_accounts_relation.id
            self.relation_num = game_accounts_relation.relation_num
            self.acounts_id = game_accounts_relation.acounts_id
            self.account_id = game_accounts_relation.account_id


class GameDevice(Base):
    __tablename__ = "game_device"

    id = Column(String(40), primary_key=True, info='设备ID')
    device_num = Column(Integer, info='设备序号')
    device_serialno = Column(String(40), info='设备序列号')
    device_name = Column(String(40), info='设备名称')
    device_connect = Column(String(40), info='设备连接信息')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"device_num= {self.device_num}," \
               f"device_serialno= {self.device_serialno}," \
               f"device_name= {self.device_name}," \
               f"device_connect= {self.device_connect}"

    def __init__(self, game_device: () = None, **kwargs):
        if game_device is None:
            self.id = kwargs.get('id')
            self.device_num = kwargs.get('device_num')
            self.device_serialno = kwargs.get('device_serialno')
            self.device_name = kwargs.get('device_name')
            self.device_connect = kwargs.get('device_connect')
        else:
            super().__init__(**kwargs)
            self.id = game_device.id
            self.device_num = game_device.device_num
            self.device_serialno = game_device.device_serialno
            self.device_name = game_device.device_name
            self.device_connect = game_device.device_connect


class GameGod(Base):
    __tablename__ = "game_god"

    id = Column(String(40), primary_key=True, info='ID')
    god_number = Column(Integer, info='式神类型内序号')
    god_name = Column(String(40), info='式神名称')
    god_type = Column(String(40), info='式神类型')
    god_sort = Column(Integer, info='式神优先级排序')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"god_number= {self.god_number}," \
               f"god_name= {self.god_name}," \
               f"god_type= {self.god_type}," \
               f"god_sort= {self.god_sort}"

    def __init__(self, game_god: () = None, **kwargs):
        if game_god is None:
            self.id = kwargs.get('id')
            self.god_number = kwargs.get('god_number')
            self.god_name = kwargs.get('god_name')
            self.god_type = kwargs.get('god_type')
            self.god_sort = kwargs.get('god_sort')
        else:
            super().__init__(**kwargs)
            self.id = game_god.id
            self.god_number = game_god.god_number
            self.god_name = game_god.god_name
            self.god_type = game_god.god_type
            self.god_sort = game_god.god_sort


class GameJob(Base):
    __tablename__ = "game_job"

    id = Column(String(40), primary_key=True, info='任务标识')
    device_id = Column(String(40), info='设备标识')
    account_ids = Column(String(40), info='账号标识组')
    job_num = Column(Integer, info='任务序号')
    week = Column(String(20), info='星期')
    start_hour = Column(Integer, info='开始时间')
    end_hour = Column(Integer, info='结束时间')
    projects_id = Column(String(40), info='项目组标识')
    project_id = Column(String(40), info='项目标识')
    timeout_hour = Column(DECIMAL(2, 1), info='超时')
    fight_times = Column(Integer, info='战斗次数')
    active_ind = Column(Integer, info='有效标志')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"device_id= {self.device_id}," \
               f"account_ids= {self.account_ids}," \
               f"job_num= {self.job_num}," \
               f"week= {self.week}," \
               f"start_hour= {self.start_hour}," \
               f"end_hour= {self.end_hour}," \
               f"projects_id= {self.projects_id}," \
               f"project_id= {self.project_id}," \
               f"timeout_hour= {self.timeout_hour}," \
               f"fight_times= {self.fight_times}," \
               f"active_ind= {self.active_ind}"

    def __init__(self, game_job: () = None, **kwargs):
        if game_job is None:
            self.id = kwargs.get('id')
            self.device_id = kwargs.get('device_id')
            self.account_ids = kwargs.get('account_ids')
            self.job_num = kwargs.get('job_num')
            self.week = kwargs.get('week')
            self.start_hour = kwargs.get('start_hour')
            self.end_hour = kwargs.get('end_hour')
            self.projects_id = kwargs.get('projects_id')
            self.project_id = kwargs.get('project_id')
            self.timeout_hour = kwargs.get('timeout_hour')
            self.fight_times = kwargs.get('fight_times')
            self.active_ind = kwargs.get('active_ind')
        else:
            super().__init__(**kwargs)
            self.id = game_job.id
            self.device_id = game_job.device_id
            self.account_ids = game_job.account_ids
            self.job_num = game_job.job_num
            self.week = game_job.week
            self.start_hour = game_job.start_hour
            self.end_hour = game_job.end_hour
            self.projects_id = game_job.projects_id
            self.project_id = game_job.project_id
            self.timeout_hour = game_job.timeout_hour
            self.fight_times = game_job.fight_times
            self.active_ind = game_job.active_ind


class GameJobLog(Base):
    __tablename__ = "game_job_log"

    id = Column(String(40), primary_key=True, info='作业日志标识')
    job_date = Column(Date, info='作业日期')
    job_id = Column(Integer, info='作业标识')
    job_state = Column(Integer, info='作业状态')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"job_date= {self.job_date}," \
               f"job_id= {self.job_id}," \
               f"job_state= {self.job_state}"

    def __init__(self, game_job_log: () = None, **kwargs):
        if game_job_log is None:
            self.id = kwargs.get('id')
            self.job_date = kwargs.get('job_date')
            self.job_id = kwargs.get('job_id')
            self.job_state = kwargs.get('job_state')
        else:
            super().__init__(**kwargs)
            self.id = game_job_log.id
            self.job_date = game_job_log.job_date
            self.job_id = game_job_log.job_id
            self.job_state = game_job_log.job_state


class GameProject(Base):
    __tablename__ = "game_project"

    id = Column(String(40), primary_key=True, info='ID')
    project_num = Column(Integer, info='序号')
    project_name = Column(String(255), info='项目名称')
    time_stamp = Column(Integer, info='时间限制标志')
    start_time = Column(Integer, info='开始时间')
    end_time = Column(Integer, info='结束时间')
    remark = Column(String(255), info='备注')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"project_num= {self.project_num}," \
               f"project_name= {self.project_name}," \
               f"time_stamp= {self.time_stamp}," \
               f"start_time= {self.start_time}," \
               f"end_time= {self.end_time}," \
               f"remark= {self.remark}"

    def __init__(self, game_project: () = None, **kwargs):
        if game_project is None:
            self.id = kwargs.get('id')
            self.project_num = kwargs.get('project_num')
            self.project_name = kwargs.get('project_name')
            self.time_stamp = kwargs.get('time_stamp')
            self.start_time = kwargs.get('start_time')
            self.end_time = kwargs.get('end_time')
            self.remark = kwargs.get('remark')
        else:
            super().__init__(**kwargs)
            self.id = game_project.id
            self.project_num = game_project.project_num
            self.project_name = game_project.project_name
            self.time_stamp = game_project.time_stamp
            self.start_time = game_project.start_time
            self.end_time = game_project.end_time
            self.remark = game_project.remark


class GameProjectLog(Base):
    __tablename__ = "game_project_log"

    id = Column(String(40), primary_key=True, info='ID')
    project_id = Column(String(40), info='项目ID')
    account_id = Column(String(40), info='角色ID')
    device_id = Column(String(40), info='设备ID')
    result = Column(String(255), info='项目执行结果')
    cost_time = Column(BigInteger, info='项目执行耗时（秒）')
    fight_time = Column(Integer, info='项目战斗耗时（秒）')
    fight_times = Column(Integer, info='项目战斗次数')
    fight_win = Column(Integer, info='项目战斗胜利次数')
    fight_fail = Column(Integer, info='项目战斗失败次数')
    fight_avg = Column(Integer, info='项目战斗平均用时')
    create_user = Column(String(40), info='创建人')
    create_time = Column(DateTime, info='创建时间')
    update_user = Column(String(40), info='修改人')
    update_time = Column(DateTime, info='修改时间')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"project_id= {self.project_id}," \
               f"account_id= {self.account_id}," \
               f"device_id= {self.device_id}," \
               f"result= {self.result}," \
               f"cost_time= {self.cost_time}," \
               f"fight_time= {self.fight_time}," \
               f"fight_times= {self.fight_times}," \
               f"fight_win= {self.fight_win}," \
               f"fight_fail= {self.fight_fail}," \
               f"fight_avg= {self.fight_avg}," \
               f"create_user= {self.create_user}," \
               f"create_time= {self.create_time}," \
               f"update_user= {self.update_user}," \
               f"update_time= {self.update_time}"

    def __init__(self, game_project_log: () = None, **kwargs):
        if game_project_log is None:
            self.id = kwargs.get('id')
            self.project_id = kwargs.get('project_id')
            self.account_id = kwargs.get('account_id')
            self.device_id = kwargs.get('device_id')
            self.result = kwargs.get('result')
            self.cost_time = kwargs.get('cost_time')
            self.fight_time = kwargs.get('fight_time')
            self.fight_times = kwargs.get('fight_times')
            self.fight_win = kwargs.get('fight_win')
            self.fight_fail = kwargs.get('fight_fail')
            self.fight_avg = kwargs.get('fight_avg')
            self.create_user = kwargs.get('create_user')
            self.create_time = kwargs.get('create_time')
            self.update_user = kwargs.get('update_user')
            self.update_time = kwargs.get('update_time')
        else:
            super().__init__(**kwargs)
            self.id = game_project_log.id
            self.project_id = game_project_log.project_id
            self.account_id = game_project_log.account_id
            self.device_id = game_project_log.device_id
            self.result = game_project_log.result
            self.cost_time = game_project_log.cost_time
            self.fight_time = game_project_log.fight_time
            self.fight_times = game_project_log.fight_times
            self.fight_win = game_project_log.fight_win
            self.fight_fail = game_project_log.fight_fail
            self.fight_avg = game_project_log.fight_avg
            self.create_user = game_project_log.create_user
            self.create_time = game_project_log.create_time
            self.update_user = game_project_log.update_user
            self.update_time = game_project_log.update_time


class GameProjects(Base):
    __tablename__ = "game_projects"

    id = Column(String(40), primary_key=True, info='ID')
    projects_num = Column(Integer, info='序号')
    projects_name = Column(String(100), info='项目名称')
    remark = Column(String(255), info='备注')
    create_user = Column(String(40), info='创建人')
    create_time = Column(DateTime, info='创建时间')
    update_user = Column(String(40), info='修改人')
    update_time = Column(DateTime, info='修改时间')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"projects_num= {self.projects_num}," \
               f"projects_name= {self.projects_name}," \
               f"remark= {self.remark}," \
               f"create_user= {self.create_user}," \
               f"create_time= {self.create_time}," \
               f"update_user= {self.update_user}," \
               f"update_time= {self.update_time}"

    def __init__(self, game_projects: () = None, **kwargs):
        if game_projects is None:
            self.id = kwargs.get('id')
            self.projects_num = kwargs.get('projects_num')
            self.projects_name = kwargs.get('projects_name')
            self.remark = kwargs.get('remark')
            self.create_user = kwargs.get('create_user')
            self.create_time = kwargs.get('create_time')
            self.update_user = kwargs.get('update_user')
            self.update_time = kwargs.get('update_time')
        else:
            super().__init__(**kwargs)
            self.id = game_projects.id
            self.projects_num = game_projects.projects_num
            self.projects_name = game_projects.projects_name
            self.remark = game_projects.remark
            self.create_user = game_projects.create_user
            self.create_time = game_projects.create_time
            self.update_user = game_projects.update_user
            self.update_time = game_projects.update_time


class GameProjectsRelation(Base):
    __tablename__ = "game_projects_relation"

    id = Column(String(40), primary_key=True, info='项目组项目关系ID')
    projects_id = Column(String(40), info='项目组ID')
    project_id = Column(String(40), info='项目ID')
    account_id = Column(String(40), info='账号ID')
    relation_num = Column(Integer, info='关系序号')
    project_num_times = Column(Integer, info='项目执行次数')
    wait_before_time = Column(BigInteger, info='项目执行前等待时间')
    wait_after_time = Column(BigInteger, info='项目执行后等待时间')
    project_state = Column(Integer, info='启用状态')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"projects_id= {self.projects_id}," \
               f"project_id= {self.project_id}," \
               f"account_id= {self.account_id}," \
               f"relation_num= {self.relation_num}," \
               f"project_num_times= {self.project_num_times}," \
               f"wait_before_time= {self.wait_before_time}," \
               f"wait_after_time= {self.wait_after_time}," \
               f"project_state= {self.project_state}"

    def __init__(self, game_projects_relation: () = None, **kwargs):
        if game_projects_relation is None:
            self.id = kwargs.get('id')
            self.projects_id = kwargs.get('projects_id')
            self.project_id = kwargs.get('project_id')
            self.account_id = kwargs.get('account_id')
            self.relation_num = kwargs.get('relation_num')
            self.project_num_times = kwargs.get('project_num_times')
            self.wait_before_time = kwargs.get('wait_before_time')
            self.wait_after_time = kwargs.get('wait_after_time')
            self.project_state = kwargs.get('project_state')
        else:
            super().__init__(**kwargs)
            self.id = game_projects_relation.id
            self.projects_id = game_projects_relation.projects_id
            self.project_id = game_projects_relation.project_id
            self.account_id = game_projects_relation.account_id
            self.relation_num = game_projects_relation.relation_num
            self.project_num_times = game_projects_relation.project_num_times
            self.wait_before_time = game_projects_relation.wait_before_time
            self.wait_after_time = game_projects_relation.wait_after_time
            self.project_state = game_projects_relation.project_state
