# coding=utf-8

'''
实现发送邮件
import smtplib
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # SMTP服务器
mail_user = "username"  # 用户名
mail_pass = "passwd"  # 密码(这里的密码不是登录邮箱密码，而是授权码)

sender = 'sender_mail@163.com'  # 发件人邮箱
receivers = ['receive_mail@qq.com']  # 接收人邮箱


content = 'Python Send Mail !'
title = 'Python SMTP Mail Test'  # 邮件主题
message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)
message['Subject'] = title

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)  # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    print("mail has been send successfully.")
except smtplib.SMTPException as e:
    print(e)

'''

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

# 第1步：连接并登录到smtp服务器
smtp = smtplib.SMTP(host='192.168.1.11')
smtp.login(user='gaokangkang', password='gk40180')

# 第2步构建一封带附件的邮件，创建一封多组件的邮件
msg = MIMEMultipart()
# 添加发件人
msg['From'] = "<gaokangkang@dvt.dvt.com>"
# 添加收件人
msg['To'] = "<zhaochanghe1@dvt.dvt.com>;<gaokangkang@dvt.dvt.com>"
# 添加标题
msg['Subject'] = Header("xxx版本测试报告", charset='utf-8')

# 添加邮件文本内容，创建邮件文件内容对象
text_content = MIMEText('''大家好：
    版本测试已完成；具体测试结果见附件；
        谢谢！''', _charset='utf-8')

# 添加附件
with open('12345.html', 'rb') as f:
    f_msg = f.read()
app = MIMEApplication(f_msg)
app.add_header('content-disposition', 'attachment', filename='python.html')

# 把邮件的文本内容和附件，添加到多组件的邮件中
msg.attach(text_content)
msg.attach(app)

# 发送邮件
smtp.send_message(msg=msg, from_addr="gaokangkang@dvt.dvt.com",
                  to_addrs=['gaokangkang@dvt.dvt.com', 'zhaochanghe1@dvt.dvt.com'])
smtp.quit()
print('send successfully')


