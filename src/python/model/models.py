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
    create_time = Column(DateTime, comment='创建时间', default=datetime.now)
    update_user = Column(VARCHAR(40), comment='修改人')
    update_time = Column(DateTime, comment='修改时间', default=datetime.now, onupdate=datetime.now())

    def __repr__(self):
        """重写显示方法，定义后查询时可以显示数据，不会显示内存地址"""
        Id = self.id
        ip = self.ip
        host_name = self.host_name
        thread_state = self.thread_state
        create_user = self.create_user
        create_time = self.create_time
        update_user = self.update_user
        update_time = self.update_time
        return f"id:{Id}, ip:{ip}, host_name:{host_name}, thread_state:{thread_state}, create_user:{create_user}," \
               f"create_time :{create_time},update_user :{create_user},update_user :{update_user}," \
               f"update_time:{update_time}"
