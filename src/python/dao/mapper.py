import configparser
import uuid
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


def select_by_id(thread_id: str) -> GameThread:
    game_thread = session.get(GameThread,thread_id)
    print(session.get(GameThread,thread_id))
    return game_thread


if __name__ == '__main__':
    # 保存测试
    # sid = str(uuid.uuid1())
    # game_thread1 = GameThread(id=str(uuid.uuid1()), ip="1")
    # save(game_thread1)
    # 查询测试
    game_thread1 = select_by_id("95cdade8-eee1-11ed-b1a8-744ca19b639c")

