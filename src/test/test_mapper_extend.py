from unittest import TestCase

from src.dao.mapper_extend import MapperExtend
from src.utils.my_logger import my_logger as logger


class TestModelsExtend(TestCase):
    def test_select_task(self):
        # 查询测试
        task = MapperExtend.select_game_task("", "2")
        logger.info(task)

    def test_select_game_project(self):
        # 查询测试
        task = MapperExtend.select_game_project("", "")
        logger.info(task)

    def test_select_game_projects(self):
        # 查询测试
        task = MapperExtend.select_game_projects("", "")
        logger.info(task)

    def test_select_game_project_log(self):
        # 查询测试
        task = MapperExtend.select_game_project_log("")
        logger.info(task)
