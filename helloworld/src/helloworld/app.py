"""
My first application
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os



class HelloWorld(toga.App):

    def startup(self):
        """
        构造并显示Toga应用程序。
        通常，你会将应用程序添加到主内容框中。
        然后我们创建一个主窗口（名称与应用程序匹配），然后显示主窗口。
        """
        main_box = toga.Box()
        # 下面是添加按钮及设置按钮属性。
        self.button = toga.Button("点      我1", on_press=self.my_callback,
                                  style=Pack(padding=50, width=200, height=100, font_family="serif", font_size=20))
        self.button_YYS = toga.Button("启动阴阳师", on_press=self.my_callonmyoji,
                                  style=Pack(padding=50, width=200, height=100, font_family="serif", font_size=20))
        main_box.add(self.button_YYS)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def my_callback(self, widget):
        # print("my name is michael") ##这是后台打印，不会在前端显示出来，学习测试时可以自行调试
        # 下面是点击按钮触发的弹窗，前端会显示。
        self.main_window.info_dialog(
            '你好', '我是一个按钮。按钮文本是：{}，按钮id是：{}，style:{}'.format(self.button.text, self.button.id,
                                                                             self.button.style)
        )
    def my_callonmyoji(self, widget):
        # 下面是点击按钮触发的弹窗，前端会显示。
        self.main_window.info_dialog(
            '你好', '我是一个按钮。按钮文本是：{}，按钮id是：{}，style:{}'.format(self.button.text, self.button.id,
                                                                             self.button.style)
        )
        os.system('adb shell am start -n com.netease.onmyoji/com.netease.ntunisdk.external.protocol.ProtocolLauncher')

def main():
    return HelloWorld()
