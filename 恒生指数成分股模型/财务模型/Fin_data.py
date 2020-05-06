# -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql

from lxml import etree
from selenium import webdriver




def get_first_page(url):

    driver.get(url)
    html = driver.page_source
    return html



# 可以尝试第二种解析方式，更加容易做计算
def parse_stock_note(html):
    big_list = []
    selector = etree.HTML(html)
    name = selector.xpath('/html/body/div/div[5]/div[1]/div[1]/a/h1/text()')
    profits= selector.xpath('//*[@id="tableGetFinanceStandard"]/tr[6]/td/text()')
    contents = name + profits
    big_tuple = tuple(contents)
    big_list.append(big_tuple)
    return big_list









def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='hk_stock',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into hk_FinData1 (code,d1,d2,d3,d4,d5,d6,d7,d8) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass


#
if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)


    HK50 =["00001","00002","00003","00005","00006","00011","00012","00016","00017","00019","00027","00066","00083","00101","00151","00175","00267","00288","00386","00388","00669","00688","00700","00762","00823","00857","00883","00939","00941","01038","01044","01088","01093","01109","01113","01177","01299","01398","01928","01997","02007","02018","02313","02318","02319","02382","02388","02628","03328","03988"]

    for code in HK50:
        url_str = 'http://stock.finance.sina.com.cn/hkstock/finance/' + str(code) + '.html#a4'

        html = get_first_page(url_str)
        content = parse_stock_note(html)
        insertDB(content)
        print(datetime.datetime.now())

# a= ['6亿','6万','8亿']

#
# create table hk_FinData1(
# id int not null primary key auto_increment,
# code varchar(16),
# d1 varchar(20),
# d2 varchar(20),
# d3 varchar(20),
# d4 varchar(20),
# d5 varchar(20),
# d6 varchar(20),
# d7 varchar(20),
# d8 varchar(20)
# ) engine=InnoDB default charset=utf8;
# #
# #
# drop table hk_FinData1;

# re.split(r'亿|万',a)
