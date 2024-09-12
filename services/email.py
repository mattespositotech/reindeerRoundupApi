from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import smtplib
from email.mime.text import MIMEText
import services.html_builder as hb

def send_email(subject, body, recipient):
    logo_path = os.path.join(os.path.dirname(__file__), '../templates/Raindeer Roundup.png')

    sender = os.environ['EMAIL_ID']
    password = os.environ['EMAIL_PASSWORD']

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    msg.attach(MIMEText(body, 'html'))

    with open(logo_path, 'rb') as img_file:
        logo = MIMEImage(img_file.read())
        logo.add_header('Content-ID', '<reindeer-logo>')
        msg.attach(logo)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipient, msg.as_string())
    print("Message sent!")

def send_invites(roundup):
    subject = "You've Been Invited To A Reindeer Roundup!"
    roundupEmailInfo = {
        'id': roundup['_id'],
        'title': roundup['name'],
        'date': roundup['date'],
        'message': roundup['message']
    }

    for part in roundup['participants']:
        if '@test.com' not in part['email']:
            body = hb.invitation_builder(roundupEmailInfo, part['uuid'])
            send_email(subject, body, part['email'])
        else:
            print('skip')

def send_recievers(roundup):
    subject = "Discover Your Secret Santa"
    roundupEmailInfo = {
        'title': roundup['name'],
        'date': roundup['date'],
    }

    name_to_email = {participant['name']: participant['email'] for participant in roundup['participants']}

    for giver, reciever in roundup['matches'].items():
        matchInfo = {
            'giver': giver,
            'reciever': reciever
        }

        if '@test.com' not in name_to_email[giver]:
            body = hb.receiver_builder(roundupEmailInfo, matchInfo)
            send_email(subject, body, name_to_email[giver])
        else:
            print('skip')


