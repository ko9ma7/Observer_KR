import time
import smtplib
import datetime
from email.mime.text import MIMEText

from key import GMAIL_ID, GMAIL_PWD


class SMTP: 
    def __init__(self):
        self,smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self,mtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(GMAIL_ID, GMAIL_PWD)
        
        self.msg = MIMEText('Link:' + url)
        self.msg['To'] = GMAIL_ID 

    def send(self, text):



class BaseCralwer:
    def __init__(self, name):
        pass
    
    def run(self):
        pass

    def send_smtp(self):
        pass
