# @Time: 2023年08月04日 18:27
# @Author: orcakill
# @File: complex_service.py
# @Description: 复杂逻辑处理
import asyncio

from src.service.image_service import ImageService

image_service = ImageService()


class ComplexService:
    @staticmethod
    async def broder_fight_end(fight_win: str, fight_fail: str, fight_again: str, fight_quit: str):
        """
        结界战斗，结束战斗
        1、战斗胜利,退出挑战
        2、退出挑战
        3、再次挑战（只识别不点击），战斗失败
        :param fight_win: 战斗胜利
        :param fight_fail: 战斗失败
        :param fight_again:  再次挑战
        :param fight_quit:  退出挑战
        :return:
        """
        # 创建任务列表
        tasks = [broder_fight_end1(fight_win, fight_quit),
                 broder_fight_end2(fight_quit),
                 broder_fight_end3(fight_again, fight_fail)]
        # 使用gather()函数等待任务完成
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        # 取消未完成的任务
        for task in pending:
            task.cancel()

        # 等待所有任务完成
        await asyncio.gather(*done)


async def broder_fight_end1(fight_win: str, fight_quit: str):
    is_win = image_service.wait(fight_win, is_click=True)
    if is_win:
        image_service.touch(fight_quit)


async def broder_fight_end2(fight_quit: str):
    image_service.wait(fight_quit, is_click=True)


async def broder_fight_end3(fight_again: str, fight_fail: str):
    is_win = image_service.wait(fight_again, is_click=True)
    if is_win:
        image_service.touch(fight_fail)
