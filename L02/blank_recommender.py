# -*- coding: utf-8 -*-

import codecs
from math import sqrt

import blank_insertData

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class recommender:
    def __init__(self, data, k=2, metric='pearson', n=5):
        """ 初始化推荐模块
        data   训练数据
        k      K邻近算法中的值
        metric 使用何种距离计算方式
        n      推荐结果的数量
        """
        self.k = k
        self.n = n
        self.username2id = {}
        self.finderid2name = {}
        self.tagsid2name = {}

        # for some reason I want to save the name of the metric

        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        #
        # 如果data是一个字典类型，则保存下来，否则忽略
        #
        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):
        """通过产品ID获取名称"""
        if id in self.tagsid2name:
            return self.tagsid2name[id]
        else:
            return id

    def userRatings(self, id, n):
        """返回该用户评分最高的物品"""
        # 打印该用户信息
        print ("Power for " + self.finderid2name[id])
        ratings = self.data[id]

        print "该用户评论数量"
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v)
                   for (k, v) in ratings]
        # finally sort and return
        ratings.sort(key=lambda artistTuple: artistTuple[1],
                     reverse = True)
        ratings = ratings[:n]
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))

    def loadBookDB(self, path=''):

        csv_finder_seed = "blank_finder_seed.csv"

        csv_finder = "blank_finder.csv"

        csv_tags = "blank_tags.csv"

        """加载BX数据集，path是数据文件位置"""
        self.data = {} #字典
        i = 0
        #
        # 将用户种子评分数据放入self.data
        #
        f = codecs.open(path + csv_finder_seed, 'r', 'utf8')
        for line in f:
            i += 1
            #separate line into fields

            fields = line.split(',')
            user_id = fields[1] #用户id
            tags_id = fields[2] # 标签id
            # power = int(fields[3]) # 评分 转为int
            power = float(fields[3]) # 评分 转为int
            power = int(power)

            # 用户是否在 data中
            # 在就 让currRa 等于之前有的数据 currentPower[book] = rating最后操作中加上 现在这个新添加的数据
            # 不在就创建新的用户列表
            if user_id in self.data:
                currentPower = self.data[user_id]
            else:
                currentPower = {}

            currentPower[tags_id] = power # key:tags_id,value:power
            self.data[user_id] = currentPower # key:user_id,value{}

        # print self.data
        f.close()

        #
        # 将标签信息存入self.tagsid2name
        # 包括isbn号、书名、作者等
        #
        f = codecs.open(path + csv_tags, 'r', 'utf8')
        for line in f:
            i += 1
            #separate line into fields
            # print line

            fields = line.split(',')
            tags_id = fields[0] # 标签id
            tags_name = fields[1] # 标签名字

            # 字典 存储 序号 和标题作者
            self.tagsid2name[tags_id] = tags_name

        # print self.tags2name
        f.close()

        #
        #  将用户信息存入self.userid2name和self.username2id
        #

        f = codecs.open(path + csv_finder, 'r', 'utf8')
        for line in f:
            i += 1
            #print(line)
            #separate line into fields
            fields = line.split(',')
            finder_id = fields[0] # 用户序号
            finder_name = fields[1] # 用户位置

            self.finderid2name[finder_id] = finder_name
            self.username2id[finder_name] = finder_id

        # print self.userid2name
        # print self.username2id
        f.close()
        print "数据量"
        print(i)

    # 计算皮尔逊相关系数的代码
    def pearson(self, my_finder_data, other_finder_data):
        sum_xy = 0  # x * y + x * y...
        sum_x = 0  # x + x +..
        sum_y = 0  # y + y..
        sum_x2 = 0  # x2 + x2..
        sum_y2 = 0
        n = 0  # 数量

        for key in my_finder_data:
            if key in other_finder_data:
                print "key"
                print key

                n += 1
                x = my_finder_data[key]#相同标签id
                y = other_finder_data[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # 计算分母
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    # 皮尔逊查找
    def getNearestNeighbor(self, finder_id):
        """获取邻近用户"""
        print "皮尔逊查找:用户id:" + str(finder_id)

        distances = []
        for instance_other_finder_id in self.data:
            if instance_other_finder_id != finder_id:

                print "instance_other_finder_id:" + str(instance_other_finder_id)

                distance = self.fn(self.data[finder_id],
                                   self.data[instance_other_finder_id])

                print "皮尔逊：" + str(distance)
                distances.append((instance_other_finder_id, distance))
        # 按距离排序，距离近的排在前面
        distances.sort(key=lambda artistTuple: artistTuple[1],
                       reverse=True)
        return distances

    def recommend(self, finder_id):

       """返回推荐列表"""
       recommendations = {}

       # 首先，获取邻近用户
       nearest = self.getNearestNeighbor(finder_id)

       print "1.通过皮尔逊获取邻近用户数量"
       print nearest
       print len(nearest)
       print "\n"

       # 获取用户评价过的商品
       userPowerd = self.data[finder_id]

       print "2.用户" + finder_id + "有过行为的标签数量"
       print len(userPowerd)
       print "\n"

       # 计算总距离
       totalDistance = 0.0

       print "3.临近K值为"

        # 默认一个人
        # 注意 A和B只有一个标签时 会是0 出错 所以要至少两个相同的标签
       for i in range(self.k):
          totalDistance += nearest[i][1]
          print "totalDistance为："
          print totalDistance

       # 汇总K邻近用户的评分
       for i in range(self.k):
          # 计算K临近算法饼图中的每个用户比重
          weight = nearest[i][1] / totalDistance

          # 获取用户名称
          other_finder_id = nearest[i][0]

          # 获取用户评分
          other_finder_power = self.data[other_finder_id]

          print "weight:"
          print weight
          print "\n"

          print other_finder_id
          print "该用户Power数量:"
          print len(other_finder_power)
          print "\n"

          # 获得user没有发现过的标签
          for artist in other_finder_power:
             if not artist in userPowerd:
                # 如果该id不在推荐中
                if artist not in recommendations:
                   # print  "not in recommendations:" + artist
                   recommendations[artist] = (other_finder_power[artist]
                                              * weight)
                else:
                    #已经有人有了 那么权重叠加
                   # print "in recommendations:" + artist
                   recommendations[artist] = (recommendations[artist]
                                              + other_finder_power[artist]
                                              * weight)
       # 开始推荐
       # now make list from dictionary

       recommendations = list(recommendations.items())

       # 根据序列号替换成书籍标题作者
       recommendations = [(self.convertProductID2name(k), v)
                          for (k, v) in recommendations]
       # 根据评分排序并返回
       recommendations.sort(key=lambda artistTuple: artistTuple[1],
                            reverse = True)
       # 返回前n个结果
       print "推荐结果为："
       return recommendations[:self.n]


if __name__ == '__main__':

    finder_id = "1";

    r = recommender(data={})

    print "导入CSV数据------------："

    r.loadBookDB('csv/')

    print "开始为用户id为" + str(finder_id) + "的finder进行推荐------------："

    # print r.recommend('1')[1][0].decode('utf-8')
    # print r.recommend(finder_id)

    blank_insertData.insertDataBase(finder_id, r.recommend(finder_id))

    print "\n\n"

    # print "30用户打分最高的5项数据------------："

    # print r.userRatings('1', 5)

