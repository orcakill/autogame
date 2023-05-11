import configparser
from typing import Optional, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.python.model.models import GameThread

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")
url = config.get("database", "url")
engine = create_engine(url, echo=False)  # 实例化数据库连接
Session = sessionmaker(bind=engine)
session = Session()


def save(game_thread: GameThread):
    """
    游戏进程保存
    :param game_thread:
    :return:
    """
    session.merge(game_thread)
    session.commit()


def select_by_id(thread_id: str):
    game_thread = session.get(GameThread, thread_id)
    session.close()
    return game_thread


