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
    game_region = Column(String(40), info='游戏服务器')
    game_name = Column(String(40), info='角色名称')
    account_class = Column(String(40), info='账号等级')
    account_number = Column(Integer, info='账号序号')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"account_type= {self.account_type}," \
               f"account_name= {self.account_name}," \
               f"account_password= {self.account_password}," \
               f"game_region= {self.game_region}," \
               f"game_name= {self.game_name}," \
               f"account_class= {self.account_class}," \
               f"account_number= {self.account_number}"

    def __init__(self, game_account: () = None, **kwargs):
        if game_account is None:
            self.id = self.id
            self.account_type = self.account_type
            self.account_name = self.account_name
            self.account_password = self.account_password
            self.game_region = self.game_region
            self.game_name = self.game_name
            self.account_class = self.account_class
            self.account_number = self.account_number
        else:
            super().__init__(**kwargs)
            self.id = game_account.id
            self.account_type = game_account.account_type
            self.account_name = game_account.account_name
            self.account_password = game_account.account_password
            self.game_region = game_account.game_region
            self.game_name = game_account.game_name
            self.account_class = game_account.account_class
            self.account_number = game_account.account_number


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

    def __init__(self, game_projects: () = None, **kwargs):
        if game_projects is None:
            self.id = self.id
            self.projects_num = self.projects_num
            self.projects_name = self.projects_name
            self.create_user = self.create_user
            self.create_time = self.create_time
            self.update_user = self.update_user
            self.update_time = self.update_time
        else:
            super().__init__(**kwargs)
            self.id = game_projects.id
            self.projects_num = game_projects.projects_num
            self.projects_name = game_projects.projects_name
            self.create_user = game_projects.create_user
            self.create_time = game_projects.create_time
            self.update_user = game_projects.update_user
            self.update_time = game_projects.update_time


class GameProjectsRelation(Base):
    __tablename__ = "game_projects_relation"

    id = Column(String(40), primary_key=True, info='项目组项目关系ID')
    projects_id = Column(String(40), info='项目组ID')
    relation_num = Column(String(40), info='关系序号')
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

    def __init__(self, game_thread: () = None, **kwargs):
        if game_thread is None:
            self.id = self.id
            self.ip = self.ip
            self.host_name = self.host_name
            self.thread_state = self.thread_state
            self.create_user = self.create_user
            self.create_time = self.create_time
            self.update_user = self.update_user
            self.update_time = self.update_time
        else:
            super().__init__(**kwargs)
            self.id = game_thread.id
            self.ip = game_thread.ip
            self.host_name = game_thread.host_name
            self.thread_state = game_thread.thread_state
            self.create_user = game_thread.create_user
            self.create_time = game_thread.create_time
            self.update_user = game_thread.update_user
            self.update_time = game_thread.update_time


class GameThreadDetail(Base):
    __tablename__ = "game_thread_detail"

    id = Column(String(40), primary_key=True, info='游戏进程详情ID')
    thread_id = Column(String(40), info='进程ID')
    projects_id = Column(String(255), info='项目组ID')
    project_id = Column(String(40), info='项目ID')
    project_state = Column(Integer, info='项目状态')
    project_num = Column(Integer, info='项目执行次数')
    create_user = Column(String(40), info='创建人')
    create_time = Column(BigInteger, info='创建时间')
    update_user = Column(String(40), info='修改人')
    update_time = Column(BigInteger, info='修改时间')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"thread_id= {self.thread_id}," \
               f"projects_id= {self.projects_id}," \
               f"project_id= {self.project_id}," \
               f"project_state= {self.project_state}," \
               f"project_num= {self.project_num}," \
               f"create_user= {self.create_user}," \
               f"create_time= {self.create_time}," \
               f"update_user= {self.update_user}," \
               f"update_time= {self.update_time}"

    def __init__(self, game_thread_detail: () = None, **kwargs):
        if game_thread_detail is None:
            self.id = self.id
            self.thread_id = self.thread_id
            self.projects_id = self.projects_id
            self.project_id = self.project_id
            self.project_state = self.project_state
            self.project_num = self.project_num
            self.create_user = self.create_user
            self.create_time = self.create_time
            self.update_user = self.update_user
            self.update_time = self.update_time
        else:
            super().__init__(**kwargs)
            self.id = game_thread_detail.id
            self.thread_id = game_thread_detail.thread_id
            self.projects_id = game_thread_detail.projects_id
            self.project_id = game_thread_detail.project_id
            self.project_state = game_thread_detail.project_state
            self.project_num = game_thread_detail.project_num
            self.create_user = game_thread_detail.create_user
            self.create_time = game_thread_detail.create_time
            self.update_user = game_thread_detail.update_user
            self.update_time = game_thread_detail.update_time


class GameThreadPicture(Base):
    __tablename__ = "game_thread_picture"

    id = Column(String(40), primary_key=True, info='游戏进程图片ID')
    thread_id = Column(String(40), info='进程ID')
    projects_id = Column(String(40), info='项目组ID')
    project_id = Column(String(40), info='项目ID')
    project_number = Column(Integer, info='项目执行第几次')
    picture_folder = Column(String(40), info='图片文件夹')
    picture_name = Column(String(40), info='图片全称')
    detail_id = Column(String(40), info='图片详情ID')
    create_user = Column(String(40), info='创建人')
    create_time = Column(BigInteger, info='创建时间')
    update_user = Column(String(40), info='修改人')
    update_time = Column(BigInteger, info='修改时间')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"thread_id= {self.thread_id}," \
               f"projects_id= {self.projects_id}," \
               f"project_id= {self.project_id}," \
               f"project_number= {self.project_number}," \
               f"picture_folder= {self.picture_folder}," \
               f"picture_name= {self.picture_name}," \
               f"detail_id= {self.detail_id}," \
               f"create_user= {self.create_user}," \
               f"create_time= {self.create_time}," \
               f"update_user= {self.update_user}," \
               f"update_time= {self.update_time}"

    def __init__(self, game_thread_picture: () = None, **kwargs):
        if game_thread_picture is None:
            self.id = self.id
            self.thread_id = self.thread_id
            self.projects_id = self.projects_id
            self.project_id = self.project_id
            self.project_number = self.project_number
            self.picture_folder = self.picture_folder
            self.picture_name = self.picture_name
            self.detail_id = self.detail_id
            self.create_user = self.create_user
            self.create_time = self.create_time
            self.update_user = self.update_user
            self.update_time = self.update_time
        else:
            super().__init__(**kwargs)
            self.id = game_thread_picture.id
            self.thread_id = game_thread_picture.thread_id
            self.projects_id = game_thread_picture.projects_id
            self.project_id = game_thread_picture.project_id
            self.project_number = game_thread_picture.project_number
            self.picture_folder = game_thread_picture.picture_folder
            self.picture_name = game_thread_picture.picture_name
            self.detail_id = game_thread_picture.detail_id
            self.create_user = game_thread_picture.create_user
            self.create_time = game_thread_picture.create_time
            self.update_user = game_thread_picture.update_user
            self.update_time = game_thread_picture.update_time


class GameThreadResult(Base):
    __tablename__ = "game_thread_result"

    id = Column(String(40), primary_key=True, info='图片结果ID')
    detail_id = Column(String(40), info='图片详情ID')
    picture_folder = Column(String(40), info='图片文件夹')
    picture_name = Column(String(40), info='图片名称')
    create_user = Column(String(40), info='创建人')
    create_time = Column(BigInteger, info='创建时间')
    update_user = Column(String(40), info='修改人')
    update_time = Column(BigInteger, info='修改时间')

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
               f"id= {self.id}," \
               f"detail_id= {self.detail_id}," \
               f"picture_folder= {self.picture_folder}," \
               f"picture_name= {self.picture_name}," \
               f"create_user= {self.create_user}," \
               f"create_time= {self.create_time}," \
               f"update_user= {self.update_user}," \
               f"update_time= {self.update_time}"

    def __init__(self, game_thread_result: () = None, **kwargs):
        if game_thread_result is None:
            self.id = self.id
            self.detail_id = self.detail_id
            self.picture_folder = self.picture_folder
            self.picture_name = self.picture_name
            self.create_user = self.create_user
            self.create_time = self.create_time
            self.update_user = self.update_user
            self.update_time = self.update_time
        else:
            super().__init__(**kwargs)
            self.id = game_thread_result.id
            self.detail_id = game_thread_result.detail_id
            self.picture_folder = game_thread_result.picture_folder
            self.picture_name = game_thread_result.picture_name
            self.create_user = game_thread_result.create_user
            self.create_time = game_thread_result.create_time
            self.update_user = game_thread_result.update_user
            self.update_time = game_thread_result.update_time
