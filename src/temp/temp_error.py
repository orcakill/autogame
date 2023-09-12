import airtest
from airtest.core.api import connect_device


def main():
    try:
        # 创建一个AirTest对象
        device = connect_device('qgame://')

        # 获取按键对象
        key = device.get_input('key')

        # 模拟按下按键
        key.push(1)

        # 模拟释放按键
        key.push(0)
    except Exception:
        pass


if __name__ == '__main__':
    main()
