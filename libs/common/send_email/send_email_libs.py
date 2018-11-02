# --*-- coding: utf-8 --*--
# @Time     : 2018/7/15 19:30
# @Author   : Ole211
# @Site     : 
# @File     : send_email_libs.py    
# @Software : PyCharm

import traceback

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header

username = "594542251@qq.com"               #qq 账户
authorization_code = "agokwajqivckbdhg"     #qq邮箱授权码
from_email = "594542251@qq.com"

def send_qq_plain_email(from_email, to_emails, title, content):
    """01发送文本邮件"""
    send_fail = []
    for to_email in to_emails:
        # 构建邮箱
        message = MIMEText(content, "plain", "utf-8")
        message ['Subject'] = "{}--邮箱测试".format(title)
        message['From'] = from_email
        message['To'] = to_email
        try:
            # 发送邮件
            s = smtplib.SMTP_SSL('smtp.qq.com', 465)
            s.login(username, authorization_code)
            s.sendemail(from_email, to_email, message.as_string())
            print(message.as_string())
            s.quit()
            print('发送成功')
        except smtplib.SMTPException, e:
            send_fail.append(to_email)
            print("发送失败， %s" % e)
    return send_fail

def send_qq_html_email(from_email, to_emails, title, content):
    """02发送html邮箱"""
    send_fail = []
    for to_email in to_emails:
        #构造邮箱
        message= MIMEText(content, "html", "utf-8")
        message['Subject'] = "{}--邮箱测试".format(title)
        message['From'] = from_email
        message['To'] = to_email
        try:
            #创建发送邮箱对象
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(username, authorization_code)
            s.sendmail(from_email, to_email, message.as_string())
            print(message.as_string())
            s.quit()
            print('发送成功')
        except smtplib.SMTPException, e:
            send_fail.append(to_email)
            print("发送失败", e)
    return send_fail

def send_qq_attach_email(from_email, to_emails, title, content, attachs):
    """03发送带有附件的链接"""
    send_fail = []
    for to_email in to_emails:
        # 创建一个带有附件的邮箱对象
        message = MIMEMultipart()
        message.attach(MIMEText(content, "html", "utf-8"))
        message['Subject'] = '{}--邮箱测试'.format(title)
        message['From'] = from_email
        message['To'] = to_email

        # 构造附件
        for f in attachs:
            attach = MIMEText(open(f, 'rb').read(), 'base64', 'utf-8')  #创建附件
            attach["Content-Type"] = 'application/octet-stream'         #创建附件请求头
            # filename 是邮件中显示的名字
            attach['content-Disposition'] = 'attchment; filename={}'.format(f)
            message.attach(attach)

        try:
            # 创建发送邮箱对象
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(username, authorization_code)
            s.sendmail(from_email, to_email, message.as_string())
            print(message.as_string())
            s.quit()
            print("发送成功")
        except smtplib.SMTPException, e:
            send_fail.append(to_email)
            print("发送失败， %s" %e)
    return send_fail

def send_qq_img_email(from_email, to_emails, title, content, attachs, imgname):
    """04发送带有图片的html邮箱"""
    send_fail = []
    for to_email in to_emails:
        #创建一个附件的实例
        message = MIMEMutipart("related")   # 生产包括多个部分的邮件， 采用related定义内嵌资源的邮件体
        message['Subject'] = "{}---邮箱测试".format(title)
        message['From'] = from_email
        message['To'] = to_email

        message_alternative = MIMEMutipart("alternative")
        message.attach(message_alternative)
        message_alternative.attach(MIMEText(content, "html", "utf-8"))

        #打开图图片
        image = open(imgname, 'rb')
        msgImage = MIMEImage(image.read())
        image.close()

        #构造附件
        for f in attachs:
            attach = MIMEText(open(f, 'rb').read(), 'base64', 'utf-8')
            attach['Content-Type'] = 'application/octet-stream'
            # filename 是邮件中显示的名字
            attach['content-Disposition'] = 'attachment;  filename={}'.format(f)
            message.attach(attach)

        try:
            # 创建发送邮箱对象
            print('----sendmail-------')
            s = smtp.SMTP_SSL("smtp.qq.com", 465)
            s.login(username, authorization_code)
            s.sendmail(from_email, to_email, message.as_string())
            s.quit()
            print('发送成功')
        except smtplib.SMTPException, e:
            send_fail.append(to_email)
            print("发送失败, %s" %e)
        except Exception, e:
            print(e)
    return send_fail

if __name__ == '__main__':
    content = """
        <p> html 邮件格式练习</p>
        <p><a href="http://www.baidu.com">百度一下</a></p>
    """
    send_qq_html_email('594542251@qq.com', '1197773452@qq.com', 'test',content)