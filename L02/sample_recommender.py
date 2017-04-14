# -*- coding: utf-8 -*-

import codecs
from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5,
                      "The Strokes": 2.5, "Vampire Weekend": 2.0},

        "Angelica2": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5,
                      "The Strokes": 2.5, "Vampire Weekend": 2.0},

         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5,
                 "Deadmau5": 4.0, "Phoenix": 2.0,
                 "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},

         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                  "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5,
                  "Slightly Stoopid": 1.0},

         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                 "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                 "Vampire Weekend": 2.0},

         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                    "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},

         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0,
                     "Norah Jones": 5.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                     "Vampire Weekend": 4.0},

         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                 "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},

         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                      "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
        }



class recommender:

    def __init__(self, data, k=1, metric='pearson', n=5):
        """ 初始化推荐模块
        data   训练数据
        k      K邻近算法中的值
        metric 使用何种距离计算方式
        n      推荐结果的数量
        """
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}

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
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    def userRatings(self, id, n):
        """返回该用户评分最高的物品"""
        # 打印该用户信息
        print ("Ratings for " + self.userid2name[id])
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
        """加载BX数据集，path是数据文件位置"""
        self.data = {}
        i = 0
        #
        # 将书籍评分数据放入self.data
        #
        f = codecs.open(path + "BX-Book-Ratings.csv", 'r', 'utf8')
        for line in f:
            i += 1
            #separate line into fields
            fields = line.split(';')
            user = fields[0].strip('"') # 用户
            book = fields[1].strip('"') # 被评分的书籍序号
            rating = int(fields[2].strip().strip('"')) # 评分

            # 用户是否在 data中
            # 在就 让currRa 等于之前有的数据 currentRatings[book] = rating最后操作中加上 现在这个新添加的数据
            # 不在就创建新的用户列表
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}

            currentRatings[book] = rating # 书籍的评分
            self.data[user] = currentRatings # 将上面的加到用户 总

        f.close()

        #
        # 将书籍信息存入self.productid2name
        # 包括isbn号、书名、作者等
        #
        f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
        for line in f:
            i += 1
            #separate line into fields
            fields = line.split(';')
            isbn = fields[0].strip('"') # 书籍序号
            title = fields[1].strip('"') # 标题
            author = fields[2].strip().strip('"') # 作者
            title = title + ' by ' + author

            # 字典 存储 序号 和标题作者
            self.productid2name[isbn] = title
        f.close()

        #
        #  将用户信息存入self.userid2name和self.username2id
        #

        f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
        for line in f:
            i += 1
            #print(line)
            #separate line into fields
            fields = line.split(';')
            userid = fields[0].strip('"') # 用户序号
            location = fields[1].strip('"') # 用户位置

            # 如果有年龄
            if len(fields) > 3:
                age = fields[2].strip().strip('"')
            else:
                age = 'NULL'
            if age != 'NULL':
                value = location + '  (age: ' + age + ')'
            else:
                value = location
            self.userid2name[userid] = value
            self.username2id[location] = userid
        f.close()
        print "数据量"
        print(i)

    # 计算皮尔逊相关系数的代码
    def pearson(self, rating1, rating2):
        sum_xy = 0  # x * y + x * y...
        sum_x = 0  # x + x +..
        sum_y = 0  # y + y..
        sum_x2 = 0  # x2 + x2..
        sum_y2 = 0
        n = 0  # 数量

        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
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
    def computeNearestNeighbor(self, username):
        """获取邻近用户"""
        distances = []
        for instance in self.data:
            if instance != username:

                # print "皮尔逊查找"

                distance = self.fn(self.data[username],
                                   self.data[instance])

                # print username + "和" + instance


                distances.append((instance, distance))
        # 按距离排序，距离近的排在前面
        distances.sort(key=lambda artistTuple: artistTuple[1],
                       reverse=True)
        return distances

    def recommend(self, user):

       """返回推荐列表"""
       recommendations = {}

       # 首先，获取邻近用户
       nearest = self.computeNearestNeighbor(user)
       print "1.通过皮尔逊获取邻近用户数量"
       print len(nearest)
       print "\n"

       # 获取用户评价过的商品
       userRatings = self.data[user]

       print "2.用户" + user + "评价过的商品数量"
       print len(userRatings)
       print "\n"

       # 计算总距离
       totalDistance = 0.0

       print "3.临近K值为"
       print self.k
       print "\n"

        # 默认一个人
       for i in range(self.k):
          totalDistance += nearest[i][1]
          print "totalDistance为："
          print nearest[i][1]

       # 汇总K邻近用户的评分
       for i in range(self.k):
          # 计算饼图的每个分片 ??
          # 计算根据什么
          weight = nearest[i][1] / totalDistance

          # 获取用户名称
          name = nearest[i][0]

          # 获取用户评分
          neighborRatings = self.data[name]

          print "weight:"
          print weight
          print "\n"

          print name
          print "该用户评分数量:"
          print len(neighborRatings)
          print "\n"

          # 获得user没有评价过的商品 根据 书籍序列号查询
          for artist in neighborRatings:
             if not artist in userRatings:
                # ？？为什么这里要判断
                # print artist
                if artist not in recommendations:
                   # print  "not in recommendations:" + artist
                   recommendations[artist] = (neighborRatings[artist]
                                              * weight)
                else:
                   # print "in recommendations:" + artist
                   recommendations[artist] = (recommendations[artist]
                                              + neighborRatings[artist]
                                              * weight)
       # 开始推荐
       # ？从这开始有点 没看
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
    # users as dataset

    print users
    r=recommender(users)

    print "开始为Angelica进行推荐------------："
    print r.recommend('Angelica')
    print "\n\n"

    print "开始为Jordyn进行推荐------------："
    print r.recommend('Jordyn')
    print "\n\n"

    print "开始为Hailey进行推荐------------："
    print r.recommend('Hailey')

    print "\n\n"

    # file as dataset
    r.loadBookDB('BX-Dump/')

    print "开始为171118进行推荐------------："

    print r.recommend('171118')

    print "\n\n"

    print "171118用户打分最高的5项数据------------："

    print r.userRatings('171118', 5)

