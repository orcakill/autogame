# coding=utf-8
import configparser
import datetime
from pathlib import Path
import uuid
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.python.utils.my_logger import MyLogger

config = configparser.ConfigParser()
project_path = Path.cwd().parent
config_path = Path(project_path.joinpath("resources"), "config.ini")
config.read(config_path, encoding="utf-8")
engine = create_engine(config.get("DATABASE", "url"), echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
metadata = Base.metadata

class GameThread(Base):
    __tablename__ = 'game_thread'

    id = Column(String(40), primary_key=True, comment='进程ID')
    ip = Column(String(40), comment='IP地址')
    host_name = Column(String(255), comment='主机名')
    thread_state = Column(Integer, comment='进程状态')
    create_user = Column(VARCHAR(40), comment='创建人')
    create_time = Column(DateTime, comment='创建时间')
    update_user = Column(VARCHAR(40), comment='修改人')
    update_time = Column(DateTime, comment='修改时间')


def model_add(game_thread: GameThread):
    session.add(game_thread)
    session.commit()


if __name__ == '__main__':
    log = MyLogger().get_logger()
    date01 = datetime.datetime.now()
    log.info(str(uuid.uuid1))
    gameThread = GameThread(id=str(uuid.uuid1))
    model_add(gameThread)
