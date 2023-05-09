import datetime

from src.python.dao.mapper import model_add
from src.python.model.models import GameThread


def test_model_add():
    date01 = datetime.datetime.now()
    gameThread = GameThread("测试", "测试", "测试", 1, "测试", date01, "测试", date01)
    model_add(gameThread)
