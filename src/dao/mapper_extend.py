from datetime import datetime, timedelta

from sqlalchemy import create_engine, or_, desc
from sqlalchemy.orm import sessionmaker

from src.model.models import GameProjects, GameProjectsRelation, GameProject, GameAccount, GameProjectLog, GameRunLog
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
            .join(GameAccount, GameAccount.id == GameProjectsRelation.user_id) \
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
    def select_region_over(day: str, game_id: str):
        """
        根据日期和用户获取当日阴阳寮突破的状态
        :param day: 日期
        :param game_id: 用户ID
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
                            .filter(GameProjectLog.role_id == game_id,
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
    def select_game_run_log(run_name: str):
        session_maker = sessionmaker(bind=engine)
        session = session_maker()
        game_run_log = (session.query(GameRunLog)
                        .filter(GameRunLog.run_name == run_name)
                        .order_by(desc(GameRunLog.run_date)).first())
        session.close()
        if game_run_log:
            return game_run_log.run_date
        else:
            return None
