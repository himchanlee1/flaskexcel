import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from myexcel import read_pickup_date
import os


def send_mail(send_from, send_to, subject, message, mtype='plain', files=[],
              server="localhost", port=587, username='', password='',
              use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        mtype (str): choose type 'plain' or 'html'
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, mtype))
 
    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment', filename=Path(path).name)
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    print('이메일 전송 완료!')
    smtp.quit()


id = '본인네이버아이디'
pw = '본인이메일비밀번호'
email = '본인이메일주소'

# 코반스 픽업요청서 양식 경로
path='form/코반스 픽업요청서 양식.xlsx'

# 네이버의 경우 server='smtp.naver.com'
# # send_mail(send_from=email, send_to=['수신자이메일주소'],
#           subject='{} 삼성서울병원 픽업 문의드립니다.'.format(read_pickup_date(file_path=path)), message=f'연구 진행 위해 픽업 문의 드립니다.', files=[path],
#           mtype='html', server='smtp.naver.com', username=email, password=pw)