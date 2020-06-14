import sys
from time import sleep
import urllib.request as ur

sys.path.append('..')
from base import BaseCralwer
from utils import config_parser, price_match


class Tmon(BaseCralwer):
    def __init__(self): # init, login, delete alert
        super().__init__()
        print('tmon crawler')  
        self.basket = []

    def _login(self):
        key = config_parser('../config/login.cfg')['tmon']
        url = 'https://login.tmon.co.kr/user/loginform?return_url='
        driver = self.get_driver()
        driver.get(url)
        driver.find_element_by_id('userid').send_keys(key['id'])
        driver.find_element_by_id('pwd').send_keys(key['pw'])
        driver.find_element_by_link_text('로그인').click()
        driver.get('http://search.tmon.co.kr') 
        # 오늘 하루 보지 않기, 1번 클릭하면 다 지워짐
        driver.find_element_by_class_name("expires").click()

    def _search(self, product_keyword):
        query='http://search.tmon.co.kr/search/?keyword={}&thr=ts'.format(product_keyword)
        page_scroll = 0
        driver = self.get_driver()
        driver.get(query)
        while len(driver.find_elements_by_class_name("item")) < 300:
            if page_scroll > 500000:
                break
            driver.execute_script("window.scrollTo(0, {})".format(page_scroll))
            page_scroll += 10000

    def _check_price(self, low, high):
        driver = self.get_driver()
        links = driver.find_elements_by_css_selector('ul > div > div > li > a')
        prices = driver.find_elements_by_css_selector('span.price > span.sale > i')
        self.basket = []
        for link_driver, price_driver in zip(links, prices):
            link = link_driver.get_attribute('href') 
            price = int(price_driver.text.replace(',',''))
            if price < low or price > high:
                continue
            self.basket.append((link, price))

    def _check_product(self, low, high):
        driver = self.get_driver()
        for link, price in self.basket:
            print(link)
            driver.get(link)
            driver.find_element_by_css_selector('#_optionScroll > div > \
                    div > div > div > button').click()
            contents = driver.find_elements_by_css_selector('#_optionScroll > \
                    div > div > div > div > ul > li')
            user_product = []
            for content in contents:
                if content.text == '':
                    break
                # price wrong..
                price = int(price_match.match(content.text).group(1).replace(',',''))
                is_valid = not content.text.endswith('매진')
                if is_valid and (low <= price <= high):
                    user_product.append(content.text)     
            print('이 link 에서 구매 가능한 물품')
            print('\n'.join(user_product))
                    
    def get_price(self): # price가 있다는 건 품절이 아니라는 것을 의미
        self._login()
        driver = self.get_driver()
        driver.get("http://www.tmon.co.kr/deal/2471909782?keyword=%EB%8B%8C%ED%85%90%EB%8F%84+%EC%8A%A4%EC%9C%84%EC%B9%98&is_ad=Y&partner_srl=943378")
        options = driver.find_elements_by_class_name("dep-sel")
        options_len = len(options) // 2
        options[0].click()  # first option open
        idx = 0
        link_product = []
        while(idx < options_len):
            for options in driver.find_elements_by_css_selector( \
                    '#_optionScroll > div > div > div > div.dep-sel.dep{}.open > ul > li'.format(idx)):
                if options.get_attribute('class') == 'soldout':
                    continue
                else:
                    link_product.append(options.text)
                    idx += 1
                    break
            idx += 1
        print(link_product)
        
    def run(self):
        self._login()
        products = config_parser('../config/product.cfg')
        print(products)
        for prod in products.values():
            self._search(prod['keyword'])
            print('search complete')
            self._check_price(prod['low_price'], prod['high_price'])
            print('check_price complete')
            self._check_product(prod['low_price'], prod['high_price'])
            print('check_product complete')
        
if __name__ == "__main__":
    a = Tmon()
    a.get_price()
    # a.run()
