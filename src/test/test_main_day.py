# @Time: 2024年01月14日 15:24
# @Author: orcakill
# @File: test_main.py
# @Description: TODO
from unittest import TestCase

from src.controller.onmyoji_controller import OnmyojiController
from src.dao.mapper import Mapper
from src.model.models import GameProjectsRelation, GameProject, GameAccount, GameProjects, GameDevices
from src.service.image_service import ImageService
from src.service.onmyoji_service import OnmyojiService
from src.service.windows_service import WindowsService
from src.utils.my_logger import logger


class TestMainDay(TestCase):

    def test_initialization(self):
        logger.info("0-6,周一、六、日，大号，日轮之陨")
        OnmyojiController.create_execute_tasks(0, '1', project_name="日轮之陨",
                                               start_hour=0, end_hour=24)