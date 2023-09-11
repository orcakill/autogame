import os

from pypinyin import pinyin, Style

from src.utils import utils_path


def get_subdirectories(folder_path):
    subdirectories = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            subdirectories.append(item_path)
    return subdirectories


if __name__ == '__main__':
    # 指定文件夹路径
    folder_path = utils_path.get_project_path()+r'\src\resources\static\onmyoji\探索\探索'

    # 获取所有文件夹
    subdirectories = get_subdirectories(folder_path)

    # 打印所有文件夹路径（去除指定路径部分）
    path = utils_path.get_project_path()+r'\src\resources\static\onmyoji\探索'
    for subdir in subdirectories:
        subdir = subdir.replace(path, "探索")
        parts = subdir.split("\\")
        result = parts[-1]

        # 使用 pinyin() 函数将中文转换为拼音
        pinyin_text = pinyin(result, style=Style.FIRST_LETTER)

        # 将拼音列表转换为字符串并转换为大写
        pinyin_text = ''.join([item[0].upper() for item in pinyin_text])

        print("explore_"+pinyin_text+"=r"+"\""+subdir+"\"")