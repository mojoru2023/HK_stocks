# -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql

from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()


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









def Python_sel_Mysql():
    # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='hk_stock',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for i in range(1,2481):
        sql = 'select code from hk_stock where id = %s ' % i
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        num = data['code']
        url = 'http://stock.finance.sina.com.cn/hkstock/finance/' + str(num) + '.html#a4'
        yield url



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
    for url_str in Python_sel_Mysql():
        html = get_first_page(url_str)
        content = parse_stock_note(html)
        insertDB(content)
        print(datetime.datetime.now())

a= ['6亿','6万','8亿']

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

re.split(r'亿|万',a)
