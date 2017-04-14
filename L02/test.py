# -*- coding: utf-8 -*-

from math import sqrt

# 字典存储评分
users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0,"Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

# “获取某个用户的评分
print users["Veronica"]
print users["Hailey"]

# 计算曼哈顿距离
def manhattan(rating1, rating2):
    """计算曼哈顿距离。rating1和rating2参数中存储的数据格式均为
    {'The Strokes': 3.0, 'Slightly Stoopid': 2.5}"""
    distance = 0
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
    return distance

print "曼哈顿距离"
print manhattan(users['Hailey'], users['Veronica'])

# 编写一个根据曼哈顿函数来找出距离最近的用户评分的东西（其实该函数会返回一个用户列表，按距离排序）
def computeNearestNeighbor(username, users):
    """计算所有用户至username用户的距离，倒序排列并返回结果列表"""
    distances = []
    for user in users:
        if user != username:
            distance = manhattan(users[user], users[username])
            distances.append((distance, user))
    # 排序 从小到大
    distances.sort()
    return distances

print "打印出Hailey最近距离的列表数据"
print computeNearestNeighbor("Hailey", users)

# 推荐A 和他相似的B 评价过的东西

def recommend(username, users):
    """返回推荐结果列表"""
    # 找到距离最近的用户
    nearest = computeNearestNeighbor(username, users)[0][1]
    recommendations = []

    # 找出这位用户评价过、但自己未曾评价的乐队
    neighborRatings = users[nearest]

    print nearest
    print neighborRatings

    userRatings = users[username]
    for artist in neighborRatings:
        if not artist in userRatings:
            recommendations.append((artist, neighborRatings[artist]))
    # 按照评分进行排序
    # 根据 a[1] 数据 倒序排序
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)

print "为Hailey推荐"
print recommend('Hailey', users)

# 闵可夫斯基距离函数
# 曼哈顿距离和欧几里得距离归纳成一个公式
# r = 1 为曼哈顿 r = 2 为欧几里得

def minkowski(rating1, rating2, r):
    distance = 0
    for key in rating1:
        if key in rating2:
            distance += pow(abs(rating1[key] - rating2[key]), r)
    return pow(distance, 1.0 / r)

# 修改computeNearestNeighbor函数中的一行
print "闵可夫斯基距离函数:欧几里得"
print minkowski(users['Hailey'], users['Veronica'], 2)
# 这里2表示使用欧几里得距离”

# 计算皮尔逊相关系数的代码
def pearson(rating1, rating2):
    sum_xy = 0 # x * y + x * y...
    sum_x = 0 # x + x +..
    sum_y = 0 # y + y..
    sum_x2 = 0 # x2 + x2..
    sum_y2 = 0
    n = 0 # 数量

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
    # 计算分母
    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator

print "测试皮尔逊函数"
print pearson(users['Angelica'], users['Bill'])



# 余弦相似度
book = {"A":{"1": 5, "2": 4, "3": 3},
        "C":{"1": 5, "2": 4, "5": 3},
        "D":{"2": 5, "3": 4},
        "Clara":{"1": 4.75, "2": 4.5, "3": 5, "4": 4.25, "5": 4},
        "Robert":{"1": 4, "2": 3, "3": 5, "4": 2, "5": 1}}

def cosineSimilarity(rating1, rating2):
    sum_x2 = 0 # x2+x2+x2
    sum_y2 = 0 # y2+y2.
    sum_xy = 0

    for key in rating1:

        x = rating1[key]
        sum_x2 += pow(x, 2)

        if key in rating2:
            # print "key:" + key
            y = rating2[key]
            sum_xy += x * y

    for key in rating2:
        # print "y:key:" + key
        y = rating2[key]
        sum_y2 += pow(y, 2)

    print sum_xy
    return sum_xy / (sqrt(sum_x2) * sqrt(sum_y2))

print "余弦相似度"
print cosineSimilarity(users['Angelica'], users['Veronica'])
print "余弦相似度"
print cosineSimilarity(book['Clara'], book['Robert'])

