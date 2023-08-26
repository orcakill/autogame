# @Time: 2023年08月26日 16:05
# @Author: orcakill
# @File: folder_utils.py
# @Description: 文件管理工具类
import os
import shutil


class FolderUtils:
    @staticmethod
    def clear_folder_shutil(path):
        shutil.rmtree(path)
        os.mkdir(path)
