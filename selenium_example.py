

# 逻辑顺序：第一页，解析代码和页数，送给翻页的页数，解析第二页 解析代码和页数
#
# 1.登录第一页
# 2.解析代码的
# 3.解析页数的
# 4.翻页操作的
# 或者55也而已，直接把要翻页的页码通过测算得到一个列表，后面直接遍历这个礼拜即可！
# 陷阱挺深，逐渐增加了好几次，到了一定程度停止下来，后面在逐渐下降！手动可以处理


# js小陷阱用点击下一页给破掉了！
# body > div.con > div > div.page > a.next
# 1.翻页正常，第一页解析正常
# 2.翻页过快。没有时间解析
# 3.用selenium请求，翻页，解析
# 翻页小陷阱，定位不准xpath ,css定位都会失效 ,一个思路就统计页码标签的个数，统计出和之后赋值给# //*[@id="tbl_wrap"]/div/a[7] b


# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql

import time
from requests.exceptions import ConnectionError
from selenium import webdriver
from lxml import etree
import datetime
driver = webdriver.Chrome()


#请求

def get_first_page():
    url = 'http://vip.stock.finance.sina.com.cn/mkt/#qbgg_hk'
    # driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    driver.set_window_size(1200, 1200)  # 设置窗口大小
    driver.get(url)
    # time.sleep(3)
    html = driver.page_source
    # time.sleep(3)
    return html


# 把首页和翻页处理？

def next_page():
    for i in range(1,62):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="tbl_wrap"]/div/a[last()]').click()
        time.sleep(3)
        html = driver.page_source
        return html




# 用遍历打开网页59次来处理

    # print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧

def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    selector = etree.HTML(html)
    code = selector.xpath('//*[@id="tbl_wrap"]/table/tbody/tr/th[1]/a/text()')
    name = selector.xpath('//*[@id="tbl_wrap"]/table/tbody/tr/th[2]/a/text()')
    for i1,i2 in zip(code,name):  # 两个列表分别遍历然后组成一个新的元组，或新的列表！
        yield (i1,i2)






#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='hk_stock',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into hk_stock (code,name) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass







if __name__ == '__main__':
        html = get_first_page()
        content = parse_html(html)
        time.sleep(3)
        insertDB(content)
        while True:
            html = next_page()
            content = parse_html(html)
            insertDB(content)
            print(datetime.datetime.now())





# 字段设置了唯一性 unique

# create table hk_stock(
# id int not null primary key auto_increment,
# code varchar(12) unique,
# name varchar(50)
# ) engine=InnoDB  charset=utf8;

# 传入url太快了，考虑分成两部分完成：1.先存到数据库中或其他容器中（数据结构不行）
#  2. 再从数据库中逐个调取进行爬取   3. 中间过渡的数据库是用内存型（redis) 还是一般存储型的？
# 4.数据量小，爬取，传入，再解析影响不大，但是分布式爬取大量数据，就必须要切割开来，才能各司其职，有效处理各自的工作！
# 5.容器是必备，分布式必备，代理池也是必备


