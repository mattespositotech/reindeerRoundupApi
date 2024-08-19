import os
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, recipients):
    sender = os.environ['EMAIL_ID']
    password = os.environ['EMAIL_PASSWORD']

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def test_email():
    subject = "Email Subject"
    body = "This is the body of the text message"
    rep = os.environ['TEST_RECIPIENT']
    recipients = [rep]
    send_email(subject, body, recipients)