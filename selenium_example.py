import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import urllib.request
import time
from multiprocessing import Pool
proxies = { "https": "https://1.199.194.227"}

headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0'}
def get_one_page(url):
    try:
        response = requests.get(url,proxies=proxies,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            get_one_page()
    except HTTPError :
        pass



start_url = ''

str_list = []

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def start_page():

    try:
        driver.get(start_url)
        # time.sleep(6)
        get_info()

    except TimeoutException:
        return start_page()



def next_page(page_number):
    try:
        # input = wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '#sub-text'))
        # )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div.con > div > div.page > a.next')))

        # input.clear()
        # input.send_keys(page_number)
        submit.click()
        # wait.until(EC.text_to_be_present_in_element(
        #     (By.CSS_SELECTOR, 'body > div.con > div > div.page > span'), str(page_number)))
        time.sleep(3)
        get_info()

    except TimeoutException:
        next_page(page_number)

# js小陷阱用点击下一页给破掉了！
# body > div.con > div > div.page > a.next
# 1.翻页正常，第一页解析正常
# 2.翻页过快。没有时间解析
# 3.用selenium请求，翻页，解析

big_list = []
url_follow = ''

def get_info():
    driver.implicitly_wait(6)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.con > div > script:nth-child(2)')))
    html = driver.page_source
    patt = re.compile('data-id="(.*?)"', re.S)
    items = re.findall(patt, html)
    for ite1 in items:
        str_list.append(ite1)
    for ite2 in iter(str_list):
        url = url_follow + ite2
        big_list.append(url)

        # for ite in iter(big_list):
        #     html = get_one_page(ite)
        #     parse_one_pic(html)



def parse_one_pic(html):
    try:
        patt = re.compile('<div class="main-image">'+'.*?<img src="(.*?)"', re.S)
        ite = re.findall(patt, html)
        for item in ite:
            try:
                urllib.request.urlretrieve(item, '/home/karson/JJJY/%s.jpg' % item[-10:-1])
            except HTTPError as e:
                print(e)
    except TypeError:
        pass
#翻页解析搞定！
if __name__ == '__main__':
    pool = Pool(6)
    start_page()
    for i in range(1,6934):
        next_page(i)
        print()
        for ite in set(big_list):
            html = get_one_page(ite)
            parse_one_pic(html)

传入url太快了，考虑分成两部分完成：1.先存到数据库中或其他容器中（数据结构不行）
 2. 再从数据库中逐个调取进行爬取   3. 中间过渡的数据库是用内存型（redis) 还是一般存储型的？
4.数据量小，爬取，传入，再解析影响不大，但是分布式爬取大量数据，就必须要切割开来，才能各司其职，有效处理各自的工作！
5.容器是必备，分布式必备，代理池也是必备

