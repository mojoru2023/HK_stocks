import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import pymysql
from lxml import etree
proxies = { "https": "https://1.199.194.227"}

headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0'}
def get_one_page(url):
    req= requests.get(url,proxies=proxies,headers=headers)
      #  requests 中文编码的终极办法！
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding

        # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        global encode_content
        encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
        return  (encode_content)

# //*[@id="tableGetFinanceStatus"]/tr[4]/th
#
# //*[@id="tableGetFinanceStatus"]/tr[5]
# //*[@id="tableGetFinanceStatus"]/tr[4]/td[4]
# tr -->td
# 比较整齐的表格用lxml的xpath可以解析！但是昨天的日股的数据结构就太乱了！果断放弃
url = 'http://stock.finance.sina.com.cn/hkstock/finance/00001.html#a4'



# 同时取三个列表中的元素放入到一个新的列表中 ,先用zip加列表解析遍历了三个列表的元素，组成一个新的元组，再把新的元组迭代如一个大列表中,代码如何插入进去
# 创建一个 叠成的列表混进去, 乘以日期元素的长度就可以变成长列表，同时遍历四个列表的同一顺序元素，再就是套路，众多元组，装在一个大列表里面，作为一个整体塞入数据库
def parse_one_page(html):
    big_list = []
    selector = etree.HTML(html)
    Dates = selector.xpath('//*[@id="tableGetBalanceSheet"]/tr[1]/td//text()')
    before_profits = selector.xpath('//*[@id="tableGetFinanceStatus"]/tr[4]/td//text()')
    after_profits = selector.xpath('//*[@id="tableGetFinanceStatus"]/tr[20]/td//text()')
    one_coding = selector.xpath('/html/body/div/div[5]/div[1]/div[1]/a/em//text()')
    codings = one_coding * len(Dates)
    long_tuple = (i for i in zip(Dates,codings,before_profits,after_profits))
    for i in long_tuple:
        big_list.append(i)
    return big_list


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




if __name__ == '__main__':
    url = 'http://stock.finance.sina.com.cn/hkstock/finance/00700.html#a4'
    html = get_one_page(url)
    content = parse_one_page(html)
    insertDB(content)

# 之前爬取A股数据时，是竖着排列，用re解析很容易插入mysql；但现在数据是横向排列，可以用lxml解析，但是需要遍历组合一下！



