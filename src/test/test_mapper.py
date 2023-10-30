from unittest import TestCase

from src.dao.mapper import Mapper
from src.model.models import GameProjectLog
from src.utils.my_logger import my_logger as logger


class TestMapper(TestCase):

    def test_select_game_account(self):
        # 查询测试
        game_account = Mapper.select_game_account("4")
        logger.info(game_account)

    def test_save_game_project_log(self):
        # 保存测试
        game_project_log = GameProjectLog()
        GameProjectLog.project_id = '1'
        Mapper.save_game_project_log(game_project_log)
