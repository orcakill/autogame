import uuid
from unittest import TestCase

from src.python.dao.mapper import save, select_by_id
from src.python.model.models import GameThread
from src.python.utils.my_logger import logger


class Test(TestCase):
    def test_save_game_thread(self):
        sid = str(uuid.uuid1())
        game_thread1 = GameThread(id=sid, ip="1")
        save(game_thread1)

    def test_select_by_id_game_thread(self):
        # 查询测试
        game_thread1 = select_by_id("95cdade8-eee1-11ed-b1a8-744ca19b639c")
        logger.info(vars(game_thread1))