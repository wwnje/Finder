#coding:utf -8

import codecs
import csv

file_name = 'csv_test.csv'
# 写入csv
csvfile = file(file_name, 'wb')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
writer.writerow(['序号;"姓名"', '年龄', '电话'])

data = [
('1;jack', ';25', ';1234567'),
('2;alice', ';18', ';789456'),
('3;tom', ';18', ';789456'),
]
writer.writerows(data)

csvfile.close()

# wb中的w表示写入模式，b是文件模式
# 写入一行用writerow
# 多行用writerows


# 读取csv
csvfile = codecs.open(file_name, 'r', 'utf-8')

for line in csvfile:
    fields = line.split(';')

    user = fields[1].strip(',')

    print fields
    print line
    print "user:"
    print user
    print

csvfile.close()