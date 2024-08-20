import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Gmail 配置信息
gmail_user = 'longtian3129@gmail.com'
gmail_password = 'wwspticuarekiloy'  # 使用应用密码

# 收件人和邮件内容
to_email = '448704865@qq.com'
subject = 'Test Email from Python'
body = 'This is a test email sent from Python!'

# 创建邮件对象
msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to_email
msg['Subject'] = subject

# 添加邮件正文
msg.attach(MIMEText(body, 'plain'))

# 连接到 Gmail SMTP 服务器并发送邮件
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    text = msg.as_string()
    server.sendmail(gmail_user, to_email, text)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
