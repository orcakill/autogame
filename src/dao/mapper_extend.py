from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from src.model.models import GameProjects, GameProjectsRelation, GameProject, GameAccount, GameProjectLog
from src.utils.utils_path import get_database_url

url = get_database_url()
engine = create_engine(url, echo=False)  # 实例化数据库连接


class MapperExtend:
    @staticmethod
    def select_game_task(object_id: str, object_projects_num: str):
        Session = sessionmaker(bind=engine)
        session = Session()
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
    def select_game_project(game_project_id: str, game_project_num: str):
        Session = sessionmaker(bind=engine)
        session = Session()
        game_project = (session.query(GameProject)
                        .filter(or_(GameProject.id == game_project_id, game_project_id == ""),
                                or_(GameProject.project_num == game_project_num, game_project_num == ""))
                        .order_by(GameProject.project_num)
                        .all())
        session.close()
        return game_project

    @staticmethod
    def select_game_projects(game_projects_id: str, game_projects_num: str):
        Session1 = sessionmaker(bind=engine)
        session = Session1()
        game_projects = (session.query(GameProjects)
                         .filter(or_(GameProjects.id == game_projects_id, game_projects_id == ""),
                                 or_(GameProjects.projects_num == game_projects_num, game_projects_num == ""))
                         .order_by(GameProjects.projects_num)
                         .all())
        session.close()
        return game_projects

    @staticmethod
    def select_game_project_log(game_project_log_id: str):
        Session1 = sessionmaker(bind=engine)
        session = Session1()
        game_project_log = (session.query(GameProjectLog)
                            .filter(or_(GameProjectLog.id == game_project_log_id, game_project_log_id == ""))
                            .order_by(GameProjectLog.create_time)
                            .all())
        session.close()
        return game_project_log
