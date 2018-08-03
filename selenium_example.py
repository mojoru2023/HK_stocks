import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import urllib.request
import time
import pymysql
from multiprocessing import Pool
proxies = { "https": "https://1.199.194.227"}

headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0'}
def get_one_page1(url):
    try:
        response = requests.get(url,proxies=proxies,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            get_one_page()
    except HTTPError :
        pass



start_url = 'http://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk'

str_list = []

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

def start_page():

    try:
        driver.get(start_url)
        time.sleep(3)
        get_info()

    except TimeoutException:
        return start_page()


def next_page():
    pageNumbers = [6, 7, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                   9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 7, 6]
    for pageNumber in iter(pageNumbers):
        submit = wait.until(
            EC.element_to_be_clickable((By.,'#tbl_wrap > div > a:nth-child(%s)'% pageNumber)))
        submit.click()
        time.sleep(3)
        driver.implicitly_wait(6)
        html = driver.page_source
        patt = re.compile(
            '<a href="http://stock.finance.sina.com.cn/hkstock/quotes/.*?.html" target="_blank">(.*?)</a></th><th><a href="http://stock.finance.sina.com.cn/hkstock/quotes/.*?.html" target="_blank">',
            re.S)
        items = re.findall(patt, html)
        for item in items:



# 逻辑顺序：第一页，解析代码和页数，送给翻页的页数，解析第二页 解析代码和页数
#
# 1.登录第一页
# 2.解析代码的
# 3.解析页数的
# 4.翻页操作的
# 或者55也而已，直接把要翻页的页码通过测算得到一个列表，后面直接遍历这个礼拜即可！
# 陷阱挺深，逐渐增加了好几次，到了一定程度停止下来，后面在逐渐下降！手动可以处理
#
# pageNumbers=[6,7,7,8,9,9,9,9,9,9,9,8,7,6]  中间再插入41个9

pageNumbers =[6, 7, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 7, 6]
需要除去第一页

# js小陷阱用点击下一页给破掉了！
# body > div.con > div > div.page > a.next
# 1.翻页正常，第一页解析正常
# 2.翻页过快。没有时间解析
# 3.用selenium请求，翻页，解析
# 翻页小陷阱，定位不准xpath ,css定位都会失效 ,一个思路就统计页码标签的个数，统计出和之后赋值给# //*[@id="tbl_wrap"]/div/a[7] b


big_list = []

# //*[@id="tbl_wrap"]/div/a[4]
# //*[@id="tbl_wrap"]/div/a[6]
# //*[@id="tbl_wrap"]/div/a[6]
# //*[@id="tbl_wrap"]/div/a[7]
def get_info():
    driver.implicitly_wait(6)
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.con > div > script:nth-child(2)')))
    html = driver.page_source
    pageNumbers = get_pageNumbers(html)
    patt = re.compile('<a href="http://stock.finance.sina.com.cn/hkstock/quotes/.*?.html" target="_blank">(.*?)</a></th><th><a href="http://stock.finance.sina.com.cn/hkstock/quotes/.*?.html" target="_blank">',re.S)
    items = re.findall(patt,html)
    for item in items:


        # big_list.append(item)
        # for ite in enumerate(big_list):
        #     print(ite)



def get_pageNumbers(html):

    return pageNUmbers


    # patt = re.compile('data-id="(.*?)"', re.S)
    # items = re.findall(patt, html)
    # for ite1 in items:
    #     str_list.append(ite1)
    # for ite2 in iter(str_list):
    #     url = url_follow + ite2
    #     big_list.append(url)

        # for ite in iter(big_list):
        #     html = get_one_page(ite)
        #     parse_one_pic(html)



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='hk_stocks',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into hk_financials (Dates,coding,before_profits,after_profits) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass




#翻页解析搞定！
if __name__ == '__main__':
    start_page()
    for i in range(2, 55):
        next_page(i)


# 传入url太快了，考虑分成两部分完成：1.先存到数据库中或其他容器中（数据结构不行）
#  2. 再从数据库中逐个调取进行爬取   3. 中间过渡的数据库是用内存型（redis) 还是一般存储型的？
# 4.数据量小，爬取，传入，再解析影响不大，但是分布式爬取大量数据，就必须要切割开来，才能各司其职，有效处理各自的工作！
# 5.容器是必备，分布式必备，代理池也是必备


