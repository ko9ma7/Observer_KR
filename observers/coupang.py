import sys
import urllib.request as ur

sys.path.append('..')
from base import BaseCralwer


class Coupang(BaseCralwer):
    def __init__(self): # init, login, delete alert
        print('coupang cralwer')

    def _login(self):
        url = 'https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F'
        driver = self.get_driver()
        driver.get(url) 

    def run(self):
        pass
        

if __name__ == "__main__":
    a = Coupang() # test
