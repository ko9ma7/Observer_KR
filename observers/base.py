import sys
import smtplib
import datetime
from time import sleep
from email.mime.text import MIMEText

from selenium import webdriver
from bs4 import BeautifulSoup as bs

sys.path.append('..')
from utils import parsingFile, getLogger


class SMTP: 
    def __init__(self):
        self.log = getLogger()
        self.user_info = parsingFile('../config/login') 
        self.login()

    def login(self):
        GMAIL_ID = self.user_info['google']['id']
        GMAIL_PWD = self.user_info['google']['pw']
        try:
            self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.login(GMAIL_ID, GMAIL_PWD)
            self.log.info('SMTP Login SUCCESS')
        except:
            self.log.error('SMTP Login FAILED')
            self.__del__()

    def __del__(self):
        self.smtp = None
            
    def send(self, mimetext: MIMEText):
        self.smtp.sendmail(GMAIL_ID, GMAIL_ID, mimetext.as_string())


class tryfindelements:
    def __init__(self, method, command):
        self.temp = None
        self.method = method
        self.command = command

    def __enter__(self):
        try_limit = 10
        while not self.temp and try_limit:
            try:
                self.temp = self.method(self.command)
            except:
                try_limit -= 1
        return self.temp

    def __exit__(self, type, value, traceback):
        pass


class BaseCralwer:
    def __init__(self):
        self.log = getLogger()
        self._driver_access()
        self._driver_init()
        self.prod_key = parsingFile('../config/product')
        self.login_key = parsingFile('../config/login')

    def __del__(self):
        self.driver.quit()
        
    def _driver_access(self):
        try:
            op = webdriver.ChromeOptions()
            # op.add_argument('headless')
            self.driver = webdriver.Chrome('/home/gunmo/public/chromedriver', 
                    options=op)
            self.driver.implicitly_wait(1)
            self.log.info('ChromeDriver Access')
        except:
            self.log.error('ChromeDriver Access Failed')

    def _driver_init(self):
        self.findE_id = self.driver.find_element_by_id
        self.findE_xp = self.driver.find_element_by_xpath
        self.findE_lt = self.driver.find_element_by_link_text
        self.findE_cn = self.driver.find_element_by_class_name
        self.findE_cs = self.driver.find_element_by_css_selector

        self.findEs_cn = self.driver.find_elements_by_class_name
        self.findEs_cs = self.driver.find_elements_by_css_selector

    def get(self, url):
        while not self.driver.current_url.startswith(url):
            self.driver.get(url)
            sleep(0.5)
        

    def scrollsTo(self, scroll_limit):
        scrolls = 0
        while scrolls < scroll_limit:
            scrolls += 10000
            self.driver.execute_script("window.scrollTo(0, {})".format(scrolls))
            sleep(0.3)

    def sendGetDatas(self):
        raise NotImplementedError

    def login(self):
        raise NotImplementedError

    # 조건(low, high)에 해당하는 product 들을 반환
    def search_products(self):
        raise NotImplementedError

    # product가 구매 가능한지를 반환
    def check_products(self):
        raise NotImplementedError
    
    # url이 구매 가능한지를 반환
    def check_urls(self):
        raise NotImplementedError

    def run(self):
        self.login()
        for prod in self.prod_key.values():
            self.search_products(prod)
            self.check_products(prod)


if __name__ == "__main__":
    a = BaseCralwer()
    del a
    b = SMTP()
    del b
