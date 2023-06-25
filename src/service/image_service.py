# @Time    : 2023年06月16日 09:15
# @Author  : orcakill
# @File    : image_service.py
# @Description : 图像识别接口
import os

from airtest.core.cv import Template

from src.service.airtest_service import AirtestService
from src.utils.my_logger import my_logger as logger
from src.utils.project_path import get_onmyoji_image_path

# 导入 airtest服务接口
airtest_service = AirtestService()


class ImageService:
    @staticmethod
    def exists(folder_path: str,cvstrategy:[]):
        """
        根据文件夹名获取图片进行图像识别，判断图片是否存在
        :param folder_path: 文件夹路径
        :return: boolean
        """
        folder_all_path = os.path.join(get_onmyoji_image_path(), folder_path)
        for file_name in os.listdir(folder_all_path):
            file_path = os.path.abspath(os.path.join(folder_all_path, file_name))
            # 判断文件是否存在
            if os.path.isfile(file_path):
                # 判断文件是否是图片类型
                file_ext = file_path.split('.')[-1].lower()
                if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                    # 图片类赋值
                    template = Template(filename=file_path)
                    # 判断图片是否存在
                    if airtest_service.assert_exists(template,cvstrategy):
                        logger.debug("图片识别成功")
                        return True
                else:
                    logger.debug("{}文件类型不为图片", file_path)
            else:
                logger.debug("{}文件不存在", file_path)
            return False
