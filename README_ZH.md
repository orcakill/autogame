# autogame <br>
# 项目目标 <br>
**自动进行游戏流程测试自动化，并生成测试报告，用于完善游戏质量，修复游戏bug。**<br>
项目视频演示地址：[点此跳转](https://www.bilibili.com/video/BV1nvtsePErk/?share_source=copy_web&vd_source=3f50e96805f688d883e5dcf9429af465)<br>
## 安装指南<br>
   1、本地安装python3.9<br>
   2、通过 pip install requirements.txt 更新本地仓库<br>
   3、执行sql脚本建立mysql数据库，sql脚本位置：/resources/autogame.sql<br>
   4、配置ini文件，格式为：
    [database]<br>
    url = mysql+pymysql://数据库用户名:数据库密码@IP:端口号/数据库名?charset=utf8<br>
    echo = True<br>
    pool_size = 10<br>
    pool_recycle = 1800<br>
    pool_timeout = 30<br>
    isolation_level = READ_COMMITTED<br>
   5、执行src/main.py或main.bat<br>
## 安装注意事项:<br>
(1)【问题】ModuleNotFoundError: No module named 'paddleocr' <br>
    【解决方案】pip install paddleocr>=2.0.1 --upgrade PyMuPDF==1.21.1 <br>
感谢JetBrains提供的支持,https://jb.gg/OpenSourceSupport<br>

