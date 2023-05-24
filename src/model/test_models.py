# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GameAccount(Base):
    __tablename__ = 'game_account'

    id = Column(String(40, 'utf8mb4_0900_ai_ci'), primary_key=True, info='ID')
    account_name = Column(String(40, 'utf8mb4_0900_ai_ci'), info='账号名称')
    account_password = Column(String(40, 'utf8mb4_0900_ai_ci'), info='账号密码')
    game_region = Column(String(40, 'utf8mb4_0900_ai_ci'), info='游戏服务器')
    game_name = Column(String(40, 'utf8mb4_0900_ai_ci'), info='角色名称')
    account_type = Column(String(40, 'utf8mb4_0900_ai_ci'), info='账号类型')
    account_class = Column(String(40, 'utf8mb4_0900_ai_ci'), info='账号等级')
    account_number = Column(Integer, info='账号序号')


class GameProject(Base):
    __tablename__ = 'game_project'

    id = Column(String(40, 'utf8mb4_0900_ai_ci'), primary_key=True, info='ID')
    project_num = Column(Integer, info='序号')
    project_name = Column(String(255, 'utf8mb4_0900_ai_ci'), info='项目名称')


class GameProjects(Base):
    __tablename__ = 'game_projects'

    id = Column(String(255), primary_key=True, info='ID')
    projects_num = Column(Integer, info='序号')
    projects_name = Column(String(255, 'utf8mb4_0900_ai_ci'), info='项目名称')
    create_user = Column(String(40, 'utf8mb4_0900_ai_ci'), info='创建人')
    create_time = Column(DateTime, info='创建时间')
    update_user = Column(String(40, 'utf8mb4_0900_ai_ci'), info='修改人')
    update_time = Column(DateTime, info='修改时间')


class GameProjectsRelation(Base):
    __tablename__ = 'game_projects_relation'

    id = Column(String(40), primary_key=True, info='项目组项目关系ID')
    projects_id = Column(String(40), info='项目组ID')
    relation_num = Column(String(40), info='关系序号')
    project_id = Column(String(40), info='项目ID')
    user_id = Column(String(40), info='用户ID')
    project_num = Column(Integer, info='项目执行次数')
    wait_before_time = Column(BigInteger, info='项目执行前等待时间')
    wait_after_time = Column(BigInteger, info='项目执行后等待时间')


class GameThread(Base):
    __tablename__ = 'game_thread'

    id = Column(String(40), primary_key=True, info='进程ID')
    ip = Column(String(40), info='IP地址')
    host_name = Column(String(255), info='主机名')
    thread_state = Column(Integer, info='进程状态')
    create_user = Column(String(40, 'utf8mb4_0900_ai_ci'), info='创建人')
    create_time = Column(DateTime, info='创建时间')
    update_user = Column(String(40, 'utf8mb4_0900_ai_ci'), info='修改人')
    update_time = Column(DateTime, info='修改时间')
