import time
import smtplib
import datetime
from email.mime.text import MIMEText

from rich import print 
from selenium import webdriver
from bs4 import BeautifulSoup as bs

class SMTP: 
    def __init__(self):
        while True:
            try:
                self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
                self.smtp.ehlo()
                self.smtp.starttls()
                self.smtp.login(GMAIL_ID, GMAIL_PWD)
                print('[bold magenta]GOOD[/bold magenta] smtp login success')
                break
            except:
                print('[bold red]BAD[/bold red] smtp login success')
                continue
            

    def send(self, mimetext: MIMEText):
        self.smtp.sendmail(GMAIL_ID, GMAIL_ID, mimetext.as_string())

class BaseCralwer:
    def __init__(self):
        print('init here')
        while True:
            try:
                op = webdriver.ChromeOptions()
                # op.add_argument('headless')
                self.driver = webdriver.Chrome('/home/gunmo/public/chromedriver', 
                        options=op)
                self.driver.implicitly_wait(10)
                print('[bold magenta]GOOD[/bold magenta] driver Chrome success')
                break
            except:
                print('[bold red]BAD[/bold red] driver Chrome success')
                continue

    def __del__(self):
        self.driver.quit()
        
    def get_driver(self):
        return self.driver
        
    def delete_alter(self):
        pass

    def run(self):
        raise NotImplementedError()


if __name__ == "__main__":
    a = BaseCralwer()
