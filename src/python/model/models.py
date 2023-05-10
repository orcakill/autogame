# coding: utf-8
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class GameThread(Base):
    __tablename__ = 'game_thread'

    id = Column(String(40), primary_key=True, comment='进程ID')
    ip = Column(String(40), comment='IP地址')
    host_name = Column(String(255), comment='主机名')
    thread_state = Column(Integer, comment='进程状态')
    create_user = Column(VARCHAR(40), comment='创建人')
    create_time = Column(DateTime, comment='创建时间',default=datetime.now)
    update_user = Column(VARCHAR(40), comment='修改人')
    update_time = Column(DateTime, comment='修改时间',default=datetime.now,onupdate=datetime.now())


# if __name__ == '__main__':
#     config = configparser.ConfigParser()
#     config.read("config.ini", encoding="utf-8")
#     url = config.get("database", "url")
#     engine = create_engine(url, echo=True)  # 实例化数据库连接
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     game_thread = GameThread(id=str(uuid.uuid1()),ip="123.1.1.1")
#     session.add(game_thread)  # 添加数据
#     session.commit()  # 最后需要调用commit()方法提交事务。

