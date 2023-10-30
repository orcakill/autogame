from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.models import GameAccount, GameProjectLog
from src.utils.utils_path import get_database_url

url = get_database_url()
engine = create_engine(url, echo=False, pool_pre_ping=True, pool_recycle=1800)  # 实例化数据库连接


class Mapper:
    @staticmethod
    def select_game_account(game_account_id: str):
        Session = sessionmaker(bind=engine)
        session = Session()
        game_account = session.get(GameAccount, game_account_id)
        session.close()
        return game_account

    @staticmethod
    def save_game_project_log(game_project_log: GameProjectLog):
        # 保存
        game_project_log1 = GameProjectLog(game_project_log)
        Session = sessionmaker(bind=engine)
        session = Session()
        if game_project_log is None:
            game_project_log1.id = uuid4()
        session.add(game_project_log)
        session.commit()
        session.close()
