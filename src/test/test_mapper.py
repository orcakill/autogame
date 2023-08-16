import uuid
from unittest import TestCase

from src.dao.mapper import save_game_thread, select_game_thread_get, select_game_account
from src.model.models import GameThread
from src.utils.my_logger import my_logger as logger


class TestMapper(TestCase):
    def test_save_game_thread(self):
        sid = str(uuid.uuid1())
        game_thread1 = GameThread(id=sid, ip="1")
        save_game_thread(game_thread1)

    def test_select_game_thread_get(self):
        # 查询测试
        game_thread1 = select_game_thread_get("2")
        logger.info(game_thread1)

    def test_select_game_account(self):
        # 查询测试
        game_account = select_game_account("4")
        logger.info(game_account)
