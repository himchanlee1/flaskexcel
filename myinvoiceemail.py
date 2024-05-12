import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path

def send_invoice_email(send_from, send_to, subject, message, mtype='plain', files=[],
              server="smtp.naver.com", port=587, username='', password='',
              use_tls=True):
    # send_from, send_to, subject, message, mtype='plain', files=[],
            #   server="smtp.naver.com", port=587, username='', password='',
            #   use_tls=True
    """Send an invoice email with an attachment.
    
    Args:
        send_from (str): Sender's email address
        send_to (str): Recipient's email address
        subject (str): Email subject
        message (str): Email body content
        username (str): SMTP server username
        password (str): SMTP server password
        server (str): SMTP server address (default to Naver)
        port (int): SMTP server port (default to 587 for Naver)
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Generate file path with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_to_send = rf'C:\Users\admin\Documents\GitHub\excel\modified_form\modified_invoice_{timestamp}.png'  # Dynamic file path

    # Attach the file
    part = MIMEBase('application', "octet-stream")
    with open(file_to_send, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{Path(file_to_send).name}"')
    msg.attach(part)

    # Send the email
    smtp = smtplib.SMTP(server, port)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
    print('Email sent successfully!')

# Example usage
if __name__ == "__main__":
    send_from = 's846464@naver.com'
    send_to = 's520212@naver.com'
    subject = 'Invoice 입니다.'
    message = '동일합니다'
    username = 's846464'
    password = 'example'

    send_invoice_email(send_from, send_to, subject, message, username, password)
