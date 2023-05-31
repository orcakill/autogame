import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from src.model.models import GameThread
from src.utils.project_path import get_project_path

root_path=get_project_path()
config_path=root_path+"src\\resources\\config.ini"
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")
url = config.get("database", "url")
engine = create_engine(url, echo=False)  # 实例化数据库连接
Session = sessionmaker(bind=engine)
session = Session()


def save_game_thread(game_thread: GameThread):
    session.merge(game_thread)
    session.commit()
    session.close()


def select_game_thread_get(id: str):
    game_thread = session.get(GameThread, id)
    session.close()
    return game_thread
