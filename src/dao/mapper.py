import datetime
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.models import GameAccount, GameProjectLog, GameDevices, GameRunLog
from src.service.windows_service import WindowsService
from src.utils.utils_path import UtilsPath

url = UtilsPath.get_database_url()
engine = create_engine(url, echo=False, pool_pre_ping=True, pool_recycle=1800)  # 实例化数据库连接


class Mapper:
    @staticmethod
    def select_game_account(game_account_id: str):
        session = sessionmaker(bind=engine)
        session1 = session()
        game_account = session1.get(GameAccount, game_account_id)
        session1.close()
        return game_account

    @staticmethod
    def save_game_project_log(game_project_log: GameProjectLog):
        # 保存
        game_project_log1 = GameProjectLog(game_project_log)
        session = sessionmaker(bind=engine)
        session1 = session()
        if game_project_log1.id is None:
            game_project_log1.id = uuid4()
            game_project_log1.create_user = WindowsService.get_computer_name(),
            game_project_log1.create_time = datetime.datetime.now()
        session1.add(game_project_log1)
        session1.commit()
        session1.close()

    @staticmethod
    def select_game_devices(game_devices_id: str):
        session = sessionmaker(bind=engine)
        session1 = session()
        game_devices = session1.get(GameDevices, game_devices_id)
        session1.close()
        return game_devices

    @staticmethod
    def save_game_run_log(game_run_log: GameRunLog):
        # 保存 game_run_log
        game_run_log1 = GameRunLog(game_run_log)
        session = sessionmaker(bind=engine)
        session1 = session()
        if game_run_log1.id is None:
            game_run_log1.id = uuid4()
        session1.add(game_run_log1)
        session1.commit()
        session1.close()
