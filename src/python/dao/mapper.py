import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import configparser

from src.python.model.models import GameThread

config = configparser.ConfigParser()
project_path = Path.cwd().parent
config_path = Path(project_path.joinpath("resources"), "config.ini")
config.read(config_path, encoding="utf-8")
engine = create_engine(config.get("database", "url"), echo=config.get("database", "echo"))
Session = sessionmaker(bind=engine)
session = Session()


def model_add(game_thread: GameThread):
    session.add(game_thread)
    session.commit()


if __name__ == '__main__':
    date01 = datetime.datetime.now()
    gameThread = GameThread("测试", "测试", "测试", 1, "测试", date01, "测试", date01)
    model_add(gameThread)
