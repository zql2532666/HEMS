import smtplib
# from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

gmail_user = "spzawiot@gmail.com"
gmail_password = "iloveIOT123"

# config = ConfigParser()
# config.read(Path(__file__).resolve().parent / 'config.ini')
# target = config['email']['target']


def create_message(sender_email, receiver_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    return message.as_string()


class EmailClient:
    def __init__(self, gmail_user, gmail_password):
        self.server = None
        self.user = gmail_user
        self.password = gmail_password

    def is_connected(self):
        try:
            status = self.server.noop()[0]
        except smtplib.SMTPServerDisconnected:
            status = -1
        return True if status == 250 else False

    def connect(self):
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.server.login(self.user, self.password)

    def send(self, to, subject, body):
        message = create_message(self.user, to, subject, body)
        try:
            self.server.sendmail(self.user, to, message)
        except:
            self.connect()
            self.server.sendmail(self.user, to, message)

    def notifyDetected(self, targets, body):
        subject = "SERVER ENVIRONMENT MONITORING SYSTEM"
        # print(body)
        for target in targets:
            print("email client loop {}".format(target))
            self.send(target, subject, body)

