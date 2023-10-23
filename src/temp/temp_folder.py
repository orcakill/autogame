import os

from pypinyin import pinyin, Style

from src.utils import utils_path


def get_subdirectories(folder_path):
    subdirectories1 = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            subdirectories1.append(item_path)
    return subdirectories1


if __name__ == '__main__':
    path_name = r'探索\章节探索'
    prefix = 'explore_'
    # 指定文件夹路径
    folder_path1 = utils_path.get_project_path() + r'src\resources\static\onmyoji\\'
    folder_path2 =folder_path1+path_name

    # 获取所有文件
    subdirectories = get_subdirectories(folder_path2)

    for subdir in subdirectories:
        subdir = subdir.replace(folder_path1, "")
        parts = subdir.split("\\")
        result = parts[-1]

        # 使用 pinyin() 函数将中文转换为拼音
        pinyin_text = pinyin(result, style=Style.FIRST_LETTER)

        # 将拼音列表转换为字符串并转换为大写
        pinyin_text = ''.join([item[0].upper() for item in pinyin_text])

        print(prefix + pinyin_text + "=r" + "\"" + subdir + "\"")
