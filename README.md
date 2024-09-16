# autogame <br>
**自动进行游戏流程测试自动化，并生成测试报告，用于完善游戏质量，修复游戏bug。**<br>
视频文件：<br>
<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=113147356650962&bvid=BV1nvtsePErk&cid=25885541868&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>
## 快速开始
   1、本地安装python3.9<br>
   2、通过 pip install requirements.txt 更新本地仓库<br>
   3、执行src/main.py或main.bat<br>
## 源码使用注意事项:<br>
(1)【问题】ModuleNotFoundError: No module named 'paddleocr' <br>
    【解决方案】pip install paddleocr>=2.0.1 --upgrade PyMuPDF==1.21.1 <br>
(2)【问题】提示缺少database<br>
    【解决方案】需配置ini文件连接数据库，需要连接MySQL库，配置模板示例<br>
    [database]<br>
    url = mysql+pymysql://数据库用户名:数据库密码@IP:端口号/数据库名?charset=utf8<br>
    echo = True<br>
    pool_size = 10<br>
    pool_recycle = 1800<br>
    pool_timeout = 30<br>
    isolation_level = READ_COMMITTED<br>
(3)【问题】缺少数据库sql文件<br>
   【解决方案】可根据models文件通过sqlalchemy包反向生成，因模型存在更新，无法及时提供最新的sql脚本<br>
感谢JetBrains提供的支持,https://jb.gg/OpenSourceSupport<br>

