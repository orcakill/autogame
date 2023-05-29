# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GameAccount(Base):
    __tablename__ = "game_account"

    id = Column(String(40), primary_key=True, info='ID')
    account_name = Column(String(40), info='账号名称')
    account_password = Column(String(40), info='账号密码')
    game_region = Column(String(40), info='游戏服务器')
    game_name = Column(String(40), info='角色名称')
    account_type = Column(String(40), info='账号类型')
    account_class = Column(String(40), info='账号等级')
    account_number = Column(Integer, info='账号序号')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"account_name= {self.account_name}," \
               f"account_password= {self.account_password}," \
               f"game_region= {self.game_region}," \
               f"game_name= {self.game_name}," \
               f"account_type= {self.account_type}," \
               f"account_class= {self.account_class}," \
               f"account_number= {self.account_number}"


class GameProject(Base):
    __tablename__ = "game_project"

    id = Column(String(40), primary_key=True, info='ID')
    project_num = Column(Integer, info='序号')
    project_name = Column(String(255), info='项目名称')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"project_num= {self.project_num}," \
               f"project_name= {self.project_name}"


class GameProjects(Base):
    __tablename__ = "game_projects"

    id = Column(String(40), primary_key=True, info='ID')
    projects_num = Column(Integer, info='序号')
    projects_name = Column(String(100), info='项目名称')
    create_user = Column(String(40), info='创建人')
    create_time = Column(DateTime, info='创建时间')
    update_user = Column(String(40), info='修改人')
    update_time = Column(DateTime, info='修改时间')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"projects_num= {self.projects_num}," \
               f"projects_name= {self.projects_name}," \
               f"create_user= {self.create_user}," \
               f"create_time= {self.create_time}," \
               f"update_user= {self.update_user}," \
               f"update_time= {self.update_time}"


class GameProjectsRelation(Base):
    __tablename__ = "game_projects_relation"

    id = Column(String(40), primary_key=True, info='项目组项目关系ID')
    projects_id = Column(String(40), info='项目组ID')
    relation_num = Column(String(40), info='关系序号')
    project_id = Column(String(40), info='项目ID')
    user_id = Column(String(40), info='用户ID')
    project_num = Column(Integer, info='项目执行次数')
    wait_before_time = Column(BigInteger, info='项目执行前等待时间')
    wait_after_time = Column(BigInteger, info='项目执行后等待时间')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"projects_id= {self.projects_id}," \
               f"relation_num= {self.relation_num}," \
               f"project_id= {self.project_id}," \
               f"user_id= {self.user_id}," \
               f"project_num= {self.project_num}," \
               f"wait_before_time= {self.wait_before_time}," \
               f"wait_after_time= {self.wait_after_time}"


class GameThread(Base):
    __tablename__ = "game_thread"

    id = Column(String(40), primary_key=True, info='进程ID')
    ip = Column(String(40), info='IP地址')
    host_name = Column(String(255), info='主机名')
    thread_state = Column(Integer, info='进程状态')
    create_user = Column(String(40), info='创建人')
    create_time = Column(DateTime, info='创建时间')
    update_user = Column(String(40), info='修改人')
    update_time = Column(DateTime, info='修改时间')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"ip= {self.ip}," \
               f"host_name= {self.host_name}," \
               f"thread_state= {self.thread_state}," \
               f"create_user= {self.create_user}," \
               f"create_time= {self.create_time}," \
               f"update_user= {self.update_user}," \
               f"update_time= {self.update_time}"
