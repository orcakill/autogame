import datetime
from uuid import uuid4

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker

from src.model.models import GameAccount, GameProjectLog, GameDevice
from src.service.windows_service import WindowsService
from src.utils.utils_path import UtilsPath

url = UtilsPath.get_database_url()
engine = create_engine(url, echo=False, pool_pre_ping=True, pool_recycle=1800)  # 实例化数据库连接


class Mapper:
    @staticmethod
    def select_game_account(game_account_id: str = "", game_account_num: str = ""):
        session = sessionmaker(bind=engine)
        session1 = session()
        game_account = (session1.query(GameAccount)
                        .filter(or_(GameAccount.id == game_account_id, game_account_id == ""),
                                or_(GameAccount.account_num == game_account_num, game_account_num == "")
                                )
                        .order_by(GameAccount.account_num)
                        .first())
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
    def select_game_device(game_device_id: str = "", game_device_num: str = ""):
        session = sessionmaker(bind=engine)
        session1 = session()
        game_device = (session1.query(GameDevice)
                       .filter(or_(GameDevice.id == game_device_id, game_device_id == ""),
                               or_(GameDevice.device_num == game_device_num, game_device_num == "")
                               )
                       .first())
        session1.close()
        return game_device
