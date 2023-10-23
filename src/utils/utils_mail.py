# @Time: 2023年10月23日 15:12
# @Author: orcakill
# @File: UtilsMail.py
# @Description: 邮件发送
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from src.utils import utils_path


def send_email(sender_name, subject, message):
    # 使用您自己的邮箱和密码发送邮件
    mail = utils_path.get_mail()
    sender_email = mail['sender_email']
    sender_password = mail['sender_password']
    recipient_email = mail['recipient_email']
    # 设置邮件内容
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = Header(sender_name, 'utf-8').encode() + ' <' + sender_email + '>'

    msg['To'] = recipient_email

    # 连接到SMTP服务器
    with smtplib.SMTP('smtp.163.com', 25) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)


if __name__ == '__main__':
    sender_name = '项目'
    subject = '项目'
    message = '这是一封测试邮件2。'
    send_email(sender_name, subject, message)
