
#coding:utf -8
import codecs
import csv
import MySQLdb
import _secret

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

host = _secret.host
root = _secret.root
pwd = _secret.pwd
dataBase = _secret.dataBase

# host = ""
# root = "root"
# pwd = ""
# dataBase = ""

csv_finder_seed = "csv/blank_finder_seed.csv"
csv_finder_seed_title = ['种子序号', 'finder_id', 'tags_id', 'power']

csv_finder = "csv/blank_finder.csv"
csv_finder_title = ['finder_id', 'name']

csv_tags = "csv/blank_tags.csv"
csv_tags_title = ['tags_id', 'tags_name']

seed_data = []
tags_data = []
finder_data = []

def insertDataBase(finder_id, data = {}):
    n = len(data)

    print "推荐给" + str(finder_id)
    print "有" + str(n) + "条数据"

    for key in data:
        print key[0].decode('utf-8')

    db = MySQLdb.connect(user=root, db=dataBase, passwd=pwd, host=host, charset='utf8')
    cursor = db.cursor()

    sql_news = "INSERT INTO sys_commend(finder_id) VALUES ('%d')" % (int(finder_id))

    try:
        # 执行sql语句
        cursor.execute(sql_news)
        # 提交到数据库执行
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    print "插入成功"

    # 关闭数据库连接
    db.close()
