import configparser

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from src.model.models import GameThread, GameProjects, GameProjectsRelation, GameProject

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")
url = config.get("database", "url")
engine = create_engine(url, echo=False)  # 实例化数据库连接
Session = sessionmaker(bind=engine)
session = Session()


class MapperExtend:
    @staticmethod
    def select_game_thread(object_id: str):
        """
        进程ID查询
        :param object_id: 进程ID
        :return: 进程信息列表
        """
        game_thread_list = session.query(GameThread).filter(or_(GameThread.id == object_id, object_id == "")).all()
        session.close()
        return game_thread_list

    @staticmethod
    def select_game_task(object_id: str, object_projects_num: str):
        task = session.query(GameProjects, GameProjectsRelation, GameProject) \
            .join(GameProjectsRelation, GameProjects.id == GameProjectsRelation.projects_id) \
            .join(GameProject, GameProjectsRelation.project_id == GameProject.id) \
            .filter(or_(GameProjects.id == object_id, object_id == ""),
                    or_(GameProjects.projects_num == object_projects_num, object_projects_num == "")) \
            .order_by(GameProjectsRelation.project_num) \
            .all()
        session.close()
        return task