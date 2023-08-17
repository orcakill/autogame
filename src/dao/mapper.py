from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.model.models import GameThread, GameAccount
from src.utils.project_path import get_database_url

url = get_database_url()
engine = create_engine(url, echo=False, pool_pre_ping=True, pool_recycle=1800)  # 实例化数据库连接


def save_game_thread(game_thread: GameThread):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.merge(game_thread)
    session.commit()
    session.close()


def select_game_thread_get(thread_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    game_thread = session.get(GameThread, thread_id)
    session.close()
    return game_thread


def select_game_account(game_account_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    game_account = session.get(GameAccount, game_account_id)
    session.close()
    return game_account
