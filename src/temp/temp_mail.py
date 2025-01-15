import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from src.utils.utils_path import UtilsPath
import numpy as np
from PIL import Image
from io import BytesIO
from src.utils.my_logger import my_logger as logger


class UtilsMail():
    @staticmethod
    def send_email(sender_name1, subject1, message1, image_arrays=None):
        # 使用您自己的邮箱和密码发送邮件
        mail = UtilsPath.get_mail()
        sender_email = mail['sender_email']
        sender_password = mail['sender_password']
        recipient_email = mail['recipient_email']
        # 设置邮件主体为 MIMEMultipart 对象
        msg = MIMEMultipart()
        # 设置 HTML 格式的邮件文本部分
        html_message = f"""
        <html>
        <body>
            <p>{message1}</p>
        </body>
        </html>
        """
        if image_arrays:
            for i, image_array in enumerate(image_arrays):
                # 将 ndarray 转换为图像
                img = Image.fromarray(image_array)
                byte_arr = BytesIO()
                img.save(byte_arr, format='PNG')
                image = MIMEImage(byte_arr.getvalue())
                image.add_header('Content-ID', f'<image{i}>')
                msg.attach(image)
                # 在 HTML 消息中添加对图片的引用
                html_message += f'<br><img src="cid:image{i}">'
        text_part = MIMEText(html_message, 'html')
        msg.attach(text_part)
        msg['Subject'] = subject1
        msg['From'] = Header(sender_name1, 'utf-8').encode() + ' <' + sender_email + '>'
        msg['To'] = recipient_email
        # SMTP 服务
        try:
            smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)  # 启用 SSL 发信，端口一般是 465
            smtpObj.login(sender_email, sender_password)  # 登录验证
            smtpObj.sendmail(sender_email, recipient_email, msg.as_string())  # 发送
            logger.debug("邮件发送成功")
        except smtplib.SMTPException as e:
            logger.exception("Error: 无法发送邮件", e)


if __name__ == '__main__':
    sender_name = '项目'
    subject = '项目1'
    message = '这是一封测试邮件2。'
    # 示例 ndarray 格式的图片，这里仅为示例，你可以替换为实际的 ndarray 图片数据
    image_array1 = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    image_array2 = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    UtilsMail.send_email(sender_name, subject, message, [image_array1, image_array2])
