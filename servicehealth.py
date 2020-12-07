# -*- coding: utf-8 -*
import requests
import email
import smtplib
import time

from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

sender = "sender"

mail_host = "mailhost"
email_user = "user"
email_pass = "password"
email_receiver = "receiver"

#发送邮件函数
def sendEmail(msg):
    # plain表示邮件内容的类型，文本类型默认是plain。utf-8表示内容的编码格式。
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = sender # 发送者
    message['To'] = email_receiver # 接收者
    message['Subject'] = "服务健康性检查" # 邮件标题
#  try:
    print "start send mail"
    smtp = smtplib.SMTP()
    smtp.connect(mail_host, 587)
    smtp.login(email_user, email_pass)
    smtp.sendmail(sender, email_receiver, message.as_string())
    smtp.quit()
#  except smtplib.SMTPException:
#    print "Error: 无法发送邮件"


request_headers = {"connection": "close"}
urls = ["http://127.0.0.1:28088/actuator/health", "http://127.0.0.1:28089/actuator/health"]
services = ["health1", "health2"]
split_str = ","

#定时轮询
#actuator /health接口返回内容：{"status":"UP"}
#每10分钟轮询一次。当服务访问不同或code!=200或status=DOWN时认为服务
while True:
    errorservice = [] #存储失败的服务
    for index,url in enumerate(urls):
        try:
			response = requests.get(url, headers = request_headers, timeout = 3)
			if response.status_code == 200:
			body = response.json()
				if body.get('status') == 'DOWN':
					errorservice.append(services[index])
			else:
				errorservice.append(services[index])
				print url+"访问失败"
	except requests.exceptions.ConnectionError:
	    errorservice.append(services[index])

    if len(errorservice) > 0:
        sendEmail(split_str.join(errorservice) + "服务访问失败或status=DOWN")
    errorservice = []
    time.sleep(60 * 10)
