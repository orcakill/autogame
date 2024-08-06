from datetime import datetime, timedelta

from sqlalchemy import create_engine, or_, desc
from sqlalchemy.orm import sessionmaker

from src.model.models import GameProjects, GameProjectsRelation, GameProject, GameAccount, GameProjectLog, GameJob, \
    GameDevice, GameAccounts, GameAccountsRelation, GameJobLog
from src.utils.utils_path import UtilsPath

url = UtilsPath.get_database_url()
engine = create_engine(url, echo=False, pool_pre_ping=True, pool_recycle=1800)  # 实例化数据库连接


class MapperExtend:
    @staticmethod
    def select_game_task(object_id: str, object_projects_num: str):
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        task = session.query(GameProjects, GameProjectsRelation, GameAccount, GameProject) \
            .join(GameProjectsRelation, GameProjects.id == GameProjectsRelation.projects_id) \
            .join(GameProject, GameProjectsRelation.project_id == GameProject.id) \
            .join(GameAccount, GameAccount.id == GameProjectsRelation.account_id) \
            .filter(or_(GameProjects.id == object_id, object_id == ""),
                    or_(GameProjects.projects_num == object_projects_num, object_projects_num == "")) \
            .order_by(GameProjects.id, GameProjectsRelation.relation_num) \
            .all()
        session.close()
        return task

    @staticmethod
    def select_game_project(game_project_id: str, game_project_num: str, game_project_name: str = ''):
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        game_project = (session.query(GameProject)
                        .filter(or_(GameProject.id == game_project_id, game_project_id == ""),
                                or_(GameProject.project_num == game_project_num, game_project_num == ""),
                                or_(GameProject.project_name == game_project_name, game_project_name == "")
                                )
                        .order_by(GameProject.project_num)
                        .all())
        session.close()
        return game_project

    @staticmethod
    def select_game_projects(game_projects_id: str, game_projects_num: str):
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        game_projects = (session.query(GameProjects)
                         .filter(or_(GameProjects.id == game_projects_id, game_projects_id == ""),
                                 or_(GameProjects.projects_num == game_projects_num, game_projects_num == ""))
                         .order_by(GameProjects.projects_num)
                         .all())
        session.close()
        return game_projects

    @staticmethod
    def select_region_over(day: str, account_id: str):
        """
        根据日期和用户获取当日阴阳寮突破的状态
        :param account_id:
        :param day: 日期
        :return: True 未攻破  False 已攻破100%
        """
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        # 将字符串转换为日期类型
        date = datetime.strptime(day, '%Y-%m-%d')
        # 创建时间对象
        time = datetime.strptime('05:00:00', '%H:%M:%S').time()
        # 将日期和时间拼接起来
        start_datetime = datetime.combine(date.date(), time)
        end_datetime = start_datetime + timedelta(days=1)
        game_project_log = (session.query(GameProjectLog)
                            .filter(GameProjectLog.account_id == account_id,
                                    GameProjectLog.result == "阴阳寮突破突破进度100%",
                                    GameProjectLog.create_time >= start_datetime,
                                    GameProjectLog.create_time <= end_datetime)
                            .all())
        session.close()
        if len(game_project_log) > 0:
            return False
        else:
            return True

    @staticmethod
    def select_game_project_log_last(device_id: str):
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        game_project_log = (session.query(GameProjectLog)
                            .filter(GameProjectLog.device_id == device_id)
                            .order_by(desc(GameProjectLog.create_time)).first())
        session.close()
        if game_project_log:
            return game_project_log.create_time
        else:
            return None

    @staticmethod
    def select_game_job_all(device_id: str):
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        game_job_all = (session.query(GameJob, GameDevice, GameAccounts, GameAccountsRelation, GameAccount)
                        .join(GameDevice, GameJob.device_id == GameDevice.id)
                        .join(GameAccounts, GameJob.account_ids == GameAccounts.id)
                        .join(GameAccountsRelation, GameAccounts.id == GameAccountsRelation.account_id)
                        .join(GameAccount, GameAccountsRelation.account_id == GameAccount.account_id)
                        .filter(or_(GameJob.device_id == device_id, device_id == ""))
                        .order_by(GameJob.device_id, GameJob.job_num, GameAccountsRelation.relation_num)
                        .all())
        session.close()
        if game_job_all:
            return game_job_all
        else:
            return None

    @staticmethod
    def select_game_job_log_all(game_job_log_id: str = "", game_job_device_id: str = "", game_job_day: str = ""):
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        # 将字符串转换为日期类型
        date = datetime.strptime(game_job_day, '%Y-%m-%d')
        game_job_log_all = (session.query(GameJob, GameJobLog)
                            .join(GameJobLog, GameJob.id == GameJobLog.job_id)
                            .filter(or_(GameJob.id == GameJob.id, game_job_log_id == ""),
                                    or_(GameJobLog.job_date == date, game_job_day == ""),
                                    or_(GameJob.device_id == game_job_device_id, game_job_device_id == ""),
                                    )
                            .all)
        session.close()
        return game_job_log_all
