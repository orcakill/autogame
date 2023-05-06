from resources.my_logger import MyLogger

if __name__ == '__main__':
    log = MyLogger().get_logger()
    log.info("脚本启动")
