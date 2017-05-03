
#coding:utf -8
import codecs
import csv
import MySQLdb
# import mysql.connector
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

# 读取数据库种子需要的数据 并保存
def readDataBase():

    # 打开数据库连接
    # db = mysql.connector.connect(host, root, pwd, dataBase)
    # 中文
    # db = MySQLdb.connect(host, root, pwd, dataBase)
    db = MySQLdb.connect(user=root, db=dataBase, passwd=pwd, host=host, charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    sql_finder_seed = "select * from finder_seed"
    sql_finder = "select * from finder"
    sql_tags = "select * from tags"

    # finder_seed
    cursor.execute(sql_finder_seed)

    # 获取全部
    results = cursor.fetchall()

    for key in results:
        seed_data.append((key[0], key[3], key[2], key[6]))

    # finder
    cursor.execute(sql_finder)
    results_finder = cursor.fetchall()
    for key in results_finder:
        finder_data.append((key[0], key[1]))

    # finder
    cursor.execute(sql_tags)
    results_tags = cursor.fetchall()

    for key in results_tags:
        tags_data.append((key[0], key[1]))
        print key[1]

    # 关闭数据库连接
    db.close()

# 根据数据创建CSV文件
def createCSV():
    # 写入csv seed
    csvfile_seed = file(csv_finder_seed, 'wb')
    csvfile_seed.write(codecs.BOM_UTF8)
    writer_seed = csv.writer(csvfile_seed)

    data = seed_data
    writer_seed.writerows(data)
    csvfile_seed.close()

    # 写入csv finder
    csvfile_finder = file(csv_finder, 'wb')
    csvfile_finder.write(codecs.BOM_UTF8)
    writer_finder = csv.writer(csvfile_finder)

    data = finder_data
    writer_finder.writerows(data)
    csvfile_finder.close()

    # 写入csv tags
    csvfile_tags = file(csv_tags, 'wb')
    csvfile_tags.write(codecs.BOM_UTF8)
    writer_tags = csv.writer(csvfile_tags)

    data = tags_data
    writer_tags.writerows(data)
    csvfile_tags.close()


def readCSV(filename):

    print
    print filename + "---------"
    # 读取csv
    csvfile = codecs.open(filename, 'r', 'utf-8')

    if(filename == csv_finder_seed):
        for line in csvfile:
            fields = line.split(',')
            # print line
            user_id = fields[1]
            tags_id = fields[2]
            power = fields[3]
            print "user_id:" + user_id
            print "tags_id:" + tags_id
            print "power:" + power

    elif(filename == csv_finder):
        for line in csvfile:
            fields = line.split(',')
            finder_id = fields[0]
            finder_name = fields[1]
            print "finder_id:" + str(finder_id)
            print "finder_name:" + finder_name

    elif(filename == csv_tags):
        for line in csvfile:
            fields = line.split(',')
            # print line
            tags_id = fields[0]
            tags_name = fields[1]
            print "tags_id:" + tags_id
            print "tags_name:" + tags_name

    print "----------------"
    csvfile.close()

readDataBase()
createCSV()

readCSV(csv_finder_seed)
readCSV(csv_finder)
readCSV(csv_tags)
