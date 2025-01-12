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
        task = MapperExtend.select_game_project("", "1")
        logger.info(task)

    def test_select_game_projects(self):
        # 查询测试
        task = MapperExtend.select_game_projects("", "")
        logger.info(task)

    def test_select_game_project_log(self):
        # 查询测试
        task = MapperExtend.select_region_over("2023-11-06", "1")
        logger.info(task)

    def test_select_game_run_log(self):
        # 查询测试
        task = MapperExtend.select_game_run_log("小号脚本")
        logger.info(task)

    def test_select_foster_carer(self):
        # 查询测试
        task = MapperExtend.select_foster_carer("2",3)
        logger.info(task)
