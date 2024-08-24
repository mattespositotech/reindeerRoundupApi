from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import smtplib
from email.mime.text import MIMEText
import services.html_builder as hb

def send_email(subject, body, recipients, image_path):
    sender = os.environ['EMAIL_ID']
    password = os.environ['EMAIL_PASSWORD']

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    msg.attach(MIMEText(body, 'html'))

    with open(image_path, 'rb') as img_file:
        image = MIMEImage(img_file.read())
        image.add_header('Content-ID', '<reindeer-logo>')
        msg.attach(image)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def test_email():
    body = hb.reciever_builder()
    subject = "You've Been Invited To A Reindeer Roundup! 5"
    rep = os.environ['TEST_RECIPIENT']
    recipients = [rep]
    image_path = os.path.join(os.path.dirname(__file__), '../templates/Raindeer Roundup.png')
    send_email(subject, body, recipients, image_path)