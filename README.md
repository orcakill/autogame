# autogame <br>
# Project Objective<br>
**Automatically conduct game process testing automation and generate test reports for improving game quality and fixing game bugs**<br>
Project video demonstration address: [Click here to jump](https://www.bilibili.com/video/BV1nvtsePErk/?share_source=copy_web&vd_source=3f50e96805f688d883e5dcf9429af465)<br>
## Installation Guide<br>
    1. Local installation of Python 3.9<br>
    2. Update local repository through pip install requirements. txt<br>
    3. Execute SQL script to establish MySQL database, SQL script location:/resources/autogame.sql<br>
    4. Configure ini file, format:<br>
        [database]<br>
        URL=mysql+pymysql://Database username: Database password @ IP: Port number/database name? charset=utf8<br>
        echo = True<br>
        pool_size = 10<br>
        pool_recycle = 1800<br>
        pool_timeout = 30<br>
        isolation_level = READ_COMMITTED<br>
    5. Execute src/main.Py or main.bat<br>
## Installation precautions:<br>
(1)【Problem】 Modulus NotFoundError: No module named 'paddleocr'<br>
   【Solution】 pip install paddleocr>=2.0.1-- upgrade PyMuPDF==1.21.1<br>
Thank you for the support provided by JetBrains, https://jb.gg/OpenSourceSupport <br>