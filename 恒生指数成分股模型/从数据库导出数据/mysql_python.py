import os

import pymysql
import csv

# 数据处理好，看如何塞入execl中


def csv_dict_write(path,head,data):
    with open(path,'w',encoding='utf-8',newline='') as f:
        writer = csv.DictWriter(f,head)
        writer.writeheader()
        writer.writerows(data)
        return True



if __name__ =='__main__':
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='hk_stock',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()

    # sql 语句
    count_sql = "select count(*) from hk_FinData1; "
    cur.execute(count_sql)
    long_count = cur.fetchone()['count(*)']
    # sql 语句
    big_list = []
    for num in range(1, long_count):


        sql = 'select code,d1,d2,d3,d4,d5,d6,d7,d8 from hk_FinData1 where id = %s ' % num
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        big_list.append(data)
    print(big_list)
    head = ['code','d1','d2','d3','d4','d5','d6','d7','d8']
    l_path = os.getcwd()
    csv_dict_write('{0}/hk50_Fdata.csv'.format(l_path),head,big_list)
    print("数据导出完成～")

