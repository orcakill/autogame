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

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"account_type= {self.account_type}," \
               f"account_name= {self.account_name}," \
               f"account_password= {self.account_password}," \
               f"role_region= {self.role_region}," \
               f"role_name= {self.role_name}," \
               f"role_class= {self.role_class}"

    def __init__(self, game_account: () = None, **kwargs):
        if game_account is None:
            self.id = self.id
            self.account_type = self.account_type
            self.account_name = self.account_name
            self.account_password = self.account_password
            self.role_region = self.role_region
            self.role_name = self.role_name
            self.role_class = self.role_class
        else:
            super().__init__(**kwargs)
            self.id = game_account.id
            self.account_type = game_account.account_type
            self.account_name = game_account.account_name
            self.account_password = game_account.account_password
            self.role_region = game_account.role_region
            self.role_name = game_account.role_name
            self.role_class = game_account.role_class


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
            self.id = self.id
            self.project_num = self.project_num
            self.project_name = self.project_name
            self.time_stamp = self.time_stamp
            self.start_time = self.start_time
            self.end_time = self.end_time
            self.remark = self.remark
        else:
            super().__init__(**kwargs)
            self.id = game_project.id
            self.project_num = game_project.project_num
            self.project_name = game_project.project_name
            self.time_stamp = game_project.time_stamp
            self.start_time = game_project.start_time
            self.end_time = game_project.end_time
            self.remark = game_project.remark


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
            self.id = self.id
            self.projects_num = self.projects_num
            self.projects_name = self.projects_name
            self.remark = self.remark
            self.create_user = self.create_user
            self.create_time = self.create_time
            self.update_user = self.update_user
            self.update_time = self.update_time
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
            self.id = self.id
            self.projects_id = self.projects_id
            self.relation_num = self.relation_num
            self.project_id = self.project_id
            self.user_id = self.user_id
            self.project_num_times = self.project_num_times
            self.wait_before_time = self.wait_before_time
            self.wait_after_time = self.wait_after_time
            self.project_state = self.project_state
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
