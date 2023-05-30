import uuid

from src.dao.mapper import save_game_thread, select_game_thread_get
from src.model.models import GameThread
from src.utils.my_logger import my_logger as logger


def test_save_game_thread():
    sid = str(uuid.uuid1())
    game_thread1 = GameThread(id=sid, ip="1")
    save_game_thread(game_thread1)


def test_select_game_thread_get():
    # 查询测试
    game_thread1 = select_game_thread_get("95cdade8-eee1-11ed-b1a8-744ca19b639c")
    logger.info(game_thread1)
