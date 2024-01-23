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

    # SMTP 服务
    try:
        smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)  # 启用 SSL 发信，端口一般是 465
        smtpObj.login(sender_email, sender_password)  # 登录验证
        smtpObj.sendmail(sender_email,recipient_email,msg.as_string())  # 发送
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)


if __name__ == '__main__':
    sender_name = '项目'
    subject = '项目1'
    message = '这是一封测试邮件2。'
    send_email(sender_name, subject, message)
