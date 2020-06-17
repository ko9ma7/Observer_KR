import sys
from time import sleep
import urllib.request as ur

from selenium.common.exceptions import NoSuchElementException

sys.path.append('..')
from base import BaseCralwer
from urls import TMON_LOGIN_URL, TMON_SEARCH_URL
from utils import parsingFile, getLogger, tm2int

class Tmon(BaseCralwer):
    def __init__(self): # init, login, delete alert
        super().__init__()
        self.log.info("TMON Observer Starting...")
        self.products = []

    def login(self):
        self.log.info("TMON Observer Login...")
        key = parsingFile('../config/login')['tmon']
        driver = self.get_driver()
        driver.get(TMON_LOGIN_URL)
        driver.find_element_by_id('userid').send_keys(key['id'])
        driver.find_element_by_id('pwd').send_keys(key['pw'])
        driver.find_element_by_link_text('로그인').click()
        driver.get('http://search.tmon.co.kr') 
        # 오늘 하루 보지 않기, 1번 클릭하면 모든 팝업 다 지워짐
        driver.find_element_by_class_name("expires").click()

    def search_products(self, prod):
        self.log.info("TMON Observer Searching Products...")

        scrolls = 0
        driver = self.get_driver()
        driver.get(TMON_SEARCH_URL.format(prod['keyword']))

        self.scrollsTo(200000)

        self.products = [] # init

        links = driver.find_elements_by_css_selector('ul > div > div > li > a')
        prices = driver.find_elements_by_css_selector('span.price > span.sale > i')
            
        for link, price in zip(links, prices):
            price = tm2int(price.text)
            if price > prod['high_price'] and price < prod['low_price']:
                continue

            self.products.append(link.get_attribute('href'))


    def check_products(self, prod):
        self.log.info("TMON Observer Checking Products...")
        datas = {'type': 'keyword'}

        for link in self.products:
            products, prices = self.check_tmon_product(link, prod)
            datas[link] = [products, prices]         
    

    def check_tmon_product(self, link, prod):
        self.log.info("TMON Observer Checking Urls:{}".format(link))

        driver = self.get_driver()
        driver.get(link)

        driver_selector = driver.find_elements_by_css_selector
        o_cssSelector = '#_optionScroll > div > div > div > div.dep-sel.dep{} > ul > li'
        options = driver.find_elements_by_class_name("dep-sel")
        o_len = len(options) // 2

        if o_len == 0:
            product = driver.find_element_by_css_selector("ul.prod > li > span.tit").text
            price = driver.find_element_by_css_selector("div.price_area > div > div > span > strong").text
            price = tm2int(price)
            if prod['low_price'] <= price <= prod['high_price']:
                return [product], [price] 
            return [], []

        o_cIdx = 0
        o_sList = [0 for _ in range(o_len)]
        options = options[:o_len]
        o_maxList = [len(driver.find_elements_by_css_selector(o_cssSelector.format(0)))//2]

        # start
        options[0].click()

        products, prices = [], []

        while True:
            # product choiced
            if o_cIdx == o_len:
                product_price, product_title = None, None
                while not (product_price and product_title):
                    try:
                        product_price = driver.find_element_by_css_selector('div.price_area > div > div > span > strong')
                        product_title = driver.find_element_by_xpath('//*[@id="_optionScroll"]/div/ul[1]/li/span[1]')
                    except NoSuchElementException:
                        self.log.warning("NoSuchElementException:product_price,product_title")
                        last_option = None
                        while not last_option:
                            try:
                                options[o_cIdx-1].click()
                                last_option = driver_selector(o_cssSelector.format( \
                                    o_cIdx-1))[o_sList[o_cIdx-1]-1]
                            except NoSuchElementException:
                                self.log.warning("NoSuchElementException:last_option")
                        last_option.click()
                product_price = tm2int(product_price.text) 
                if prod['low_price'] <= product_price <= prod['high_price']:
                    products.append(product_title.text)
                    prices.append(product_price)

                o_cIdx -= 1
                driver.find_element_by_class_name("del").click()
                options[o_cIdx].click()
                continue
            
            # option add maxlen
            if o_sList[o_cIdx] == 0 and o_cIdx != 0:
                o_maxList.append(len(driver_selector(o_cssSelector.format(o_cIdx)))//2)
                
            # option arrived maxlen
            if o_sList[o_cIdx] == o_maxList[o_cIdx]:
                o_sList[o_cIdx] = 0
                o_cIdx -= 1
                options[o_cIdx].click()
                o_maxList.pop()
                if o_maxList:
                    continue
                break
                    
            n_option = None
            while not n_option:
                try:
                    n_option = driver_selector(o_cssSelector.format(o_cIdx))[o_sList[o_cIdx]]
                except NoSuchElementException:
                    pass
                
            # option:n plus
            o_sList[o_cIdx] += 1
            
            if n_option.get_attribute('class') == 'soldout':    
                continue
                
            # option:n click
            n_option.click()
            
            # option:n to n + 1
            o_cIdx += 1

        return products, prices
    
        
    def check_urls(self):
        pass
        

if __name__ == "__main__":
    a = Tmon()
    a.run()
