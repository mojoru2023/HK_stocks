


import datetime
import time

import pymysql
import requests
from lxml import etree
import json
from queue import Queue
import threading
from requests.exceptions import RequestException






def run_forever(func):
    def wrapper(obj):
        while True:
            func(obj)
    return wrapper


def RemoveDot(item):
    f_l = []
    for it in item:

        f_str = "".join(it.split(","))
        ff_str = f_str +"00"
        f_l.append(ff_str)

    return f_l

def remove_douhao(num):
    num1 = "".join(num.split(","))
    f_num = str(num1)
    return f_num
def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items


class HKPool_M(object):

    def __init__(self,url):
        self.url = url

    def page_request(self):
        ''' 发送请求获取数据 '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }

        response = requests.get(self.url,headers=headers)
        if response.status_code == 200:
            html = response.text
            return html
        else:
            pass

    def page_parse_(self):
        '''根据页面内容使用lxml解析数据, 获取段子列表'''


        html  = self.page_request()
        element = etree.HTML(html)

        now_price = element.xpath('//*[@id="spFP"]/div[1]/span[1]/text()')
        for item in now_price:
            big_list.append(item)
        return big_list




def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='hk_stock',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    try:
        # 用一个列表解析
        f_hks = ["hk" + str(cod) for cod in HK50]
        sp_func = lambda x: ",".join(x)
        f_lcode = sp_func(f_hks)

        f_ls = "%s," * len(HK50)# 这里错了
        cursor.executemany('insert into HK_mons ({0}) values ({1})'.format(f_lcode, f_ls[:-1]), content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass








if __name__ == '__main__':
    HK50 =["00001","00002","00003","00005","00006","00011","00012","00016","00017","00019","00027","00066","00083","00101","00151","00175","00267","00288","00386","00388","00669","00688","00700","00762","00823","00857","00883","00939","00941","01038","01044","01088","01093","01109","01113","01177","01299","01398","01928","01997","02007","02018","02313","02318","02319","02382","02388","02628","03328","03988"]

    big_list = []


    for it in HK50:
        url = 'http://gu.qq.com/hk{0}/gp'.format(it)
        print(url)
        hksp = HKPool_M(url)# 这里把请求和解析都进行了处理
        hksp.page_parse_()
    ff_l = []
    f_tup = tuple(big_list)
    ff_l.append((f_tup))
    print(ff_l)
    insertDB(ff_l)
























 # create table HK_mons(id int not null primary key auto_increment, hk00001   float,hk00002   float,hk00003   float,hk00005   float,hk00006   float,hk00011   float,hk00012   float,hk00016   float,hk00017   float,hk00019   float,hk00027   float,hk00066   float,hk00083   float,hk00101   float,hk00151   float,hk00175   float,hk00267   float,hk00288   float,hk00386   float,hk00388   float,hk00669   float,hk00688   float,hk00700   float,hk00762   float,hk00823   float,hk00857   float,hk00883   float,hk00939   float,hk00941   float,hk01038   float,hk01044   float,hk01088   float,hk01093   float,hk01109   float,hk01113   float,hk01177   float,hk01299   float,hk01398   float,hk01928   float,hk01997   float,hk02007   float,hk02018   float,hk02313   float,hk02318   float,hk02319   float,hk02382   float,hk02388   float,hk02628   float,hk03328   float,hk03988   float, LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ) engine=InnoDB  charset=utf8;


