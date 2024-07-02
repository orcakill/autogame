# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GameAccount(Base):
    __tablename__ = "game_account"

    id = Column(String(40), primary_key=True, info='ID')
    account_type = Column(String(40), info='账号类型')
    account_name = Column(String(40), info='账号名称')
    account_password = Column(String(40), info='账号密码')
    role_region = Column(String(40), info='角色服务器')
    role_name = Column(String(40), info='角色名称')
    role_class = Column(String(40), info='角色等级')
    game_emaki = Column(Integer, info='绘卷模式')
    super_ghost_king = Column(Integer, info='超鬼王')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"account_type= {self.account_type}," \
               f"account_name= {self.account_name}," \
               f"account_password= {self.account_password}," \
               f"role_region= {self.role_region}," \
               f"role_name= {self.role_name}," \
               f"role_class= {self.role_class}," \
               f"game_emaki= {self.game_emaki}," \
               f"super_ghost_king= {self.super_ghost_king}"

    def __init__(self, game_account: () = None, **kwargs):
        if game_account is None:
            self.id = kwargs.get('id')
            self.account_type = kwargs.get('account_type')
            self.account_name = kwargs.get('account_name')
            self.account_password = kwargs.get('account_password')
            self.role_region = kwargs.get('role_region')
            self.role_name = kwargs.get('role_name')
            self.role_class = kwargs.get('role_class')
            self.game_emaki = kwargs.get('game_emaki')
            self.super_ghost_king = kwargs.get('super_ghost_king')
        else:
            super().__init__(**kwargs)
            self.id = game_account.id
            self.account_type = game_account.account_type
            self.account_name = game_account.account_name
            self.account_password = game_account.account_password
            self.role_region = game_account.role_region
            self.role_name = game_account.role_name
            self.role_class = game_account.role_class
            self.game_emaki = game_account.game_emaki
            self.super_ghost_king = game_account.super_ghost_king


class GameDevices(Base):
    __tablename__ = "game_devices"

    id = Column(String(40), primary_key=True, info='设备ID')
    device_serialno = Column(String(40), info='设备序列号')
    devices_name = Column(String(40), info='设备名称')
    devices_connect = Column(String(40), info='设备连接信息')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"device_serialno= {self.device_serialno}," \
               f"devices_name= {self.devices_name}," \
               f"devices_connect= {self.devices_connect}"

    def __init__(self, game_devices: () = None, **kwargs):
        if game_devices is None:
            self.id = kwargs.get('id')
            self.device_serialno = kwargs.get('device_serialno')
            self.devices_name = kwargs.get('devices_name')
            self.devices_connect = kwargs.get('devices_connect')
        else:
            super().__init__(**kwargs)
            self.id = game_devices.id
            self.device_serialno = game_devices.device_serialno
            self.devices_name = game_devices.devices_name
            self.devices_connect = game_devices.devices_connect


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
    role_id = Column(String(40), info='角色ID')
    devices_id = Column(String(40), info='设备ID')
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
               f"role_id= {self.role_id}," \
               f"devices_id= {self.devices_id}," \
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
            self.role_id = kwargs.get('role_id')
            self.devices_id = kwargs.get('devices_id')
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
            self.role_id = game_project_log.role_id
            self.devices_id = game_project_log.devices_id
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
    relation_num = Column(Integer, info='关系序号')
    project_id = Column(String(40), info='项目ID')
    user_id = Column(String(40), info='用户ID')
    project_num_times = Column(Integer, info='项目执行次数')
    wait_before_time = Column(BigInteger, info='项目执行前等待时间')
    wait_after_time = Column(BigInteger, info='项目执行后等待时间')
    project_state = Column(Integer, info='启用状态')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"projects_id= {self.projects_id}," \
               f"relation_num= {self.relation_num}," \
               f"project_id= {self.project_id}," \
               f"user_id= {self.user_id}," \
               f"project_num_times= {self.project_num_times}," \
               f"wait_before_time= {self.wait_before_time}," \
               f"wait_after_time= {self.wait_after_time}," \
               f"project_state= {self.project_state}"

    def __init__(self, game_projects_relation: () = None, **kwargs):
        if game_projects_relation is None:
            self.id = kwargs.get('id')
            self.projects_id = kwargs.get('projects_id')
            self.relation_num = kwargs.get('relation_num')
            self.project_id = kwargs.get('project_id')
            self.user_id = kwargs.get('user_id')
            self.project_num_times = kwargs.get('project_num_times')
            self.wait_before_time = kwargs.get('wait_before_time')
            self.wait_after_time = kwargs.get('wait_after_time')
            self.project_state = kwargs.get('project_state')
        else:
            super().__init__(**kwargs)
            self.id = game_projects_relation.id
            self.projects_id = game_projects_relation.projects_id
            self.relation_num = game_projects_relation.relation_num
            self.project_id = game_projects_relation.project_id
            self.user_id = game_projects_relation.user_id
            self.project_num_times = game_projects_relation.project_num_times
            self.wait_before_time = game_projects_relation.wait_before_time
            self.wait_after_time = game_projects_relation.wait_after_time
            self.project_state = game_projects_relation.project_state


class GameRunLog(Base):
    __tablename__ = "game_run_log"

    id = Column(String(40), primary_key=True, info='ID')
    run_date = Column(DateTime, info='运行时间')
    run_name = Column(String(40), info='运行名称')
    run_state = Column(Integer, info='运行状态')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"run_date= {self.run_date}," \
               f"run_name= {self.run_name}," \
               f"run_state= {self.run_state}"

    def __init__(self, game_run_log: () = None, **kwargs):
        if game_run_log is None:
            self.id = kwargs.get('id')
            self.run_date = kwargs.get('run_date')
            self.run_name = kwargs.get('run_name')
            self.run_state = kwargs.get('run_state')
        else:
            super().__init__(**kwargs)
            self.id = game_run_log.id
            self.run_date = game_run_log.run_date
            self.run_name = game_run_log.run_name
            self.run_state = game_run_log.run_state
