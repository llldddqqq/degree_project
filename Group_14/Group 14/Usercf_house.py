# coding = utf-8

# 基于用户的协同过滤推荐算法实现
import random
from pymysql import *
import math
from operator import itemgetter


class UserBasedCF():
    # 初始化相关参数
    def __init__(self):
        # 找到与目标用户兴趣相似的20个用户，为其推荐10部电影
        self.n_sim_user = 10
        self.n_rec_house = 5

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.house_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded house number = %d' % self.n_rec_house)

    # 读文件得到“用户-电影”数据

    def get_dataset(self, filename, pivot=0.75):
        #获取用户列表
        userlist=[]
        #userinfo={}
        trainSet_len = 0
        testSet_len = 0
        host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
        port = 3306
        db_user = 'dingqi'
        db_password = 'Liu18501303736'
        database = 'degree_project_db'
        conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
        cur = conn.cursor()
        sql = "select user_name from user_info"
        cur.execute(sql)
        result = cur.fetchall()
        #print(result)
        for user in result:
            userlist.append(user[0])
        #print(userlist)
        #获取用户信息
        for user in userlist:
            sql2="select saved_property from user_info where user_name='"+ user +"'"
            cur.execute(sql2)
            result = cur.fetchall()
            #print(result[0][0])
            if random.random() < pivot:
                self.trainSet.setdefault(user, {})
                self.trainSet[user][result[0][0]] = 5
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][result[0][0]] = 5
                testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)
        #print(self.trainSet,self.testSet)
    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)

    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建“电影-用户”倒排索引
        # key = houseID, value = list of userIDs who have seen this house
        print('Building house-user table ...')
        house_user = {}
        for user, houses in self.trainSet.items():
            for house in houses:
                if house not in house_user:
                    house_user[house] = set()
                house_user[house].add(user)
        print('Build house-user table success!')

        self.house_count = len(house_user)
        print('Total house number = %d' % self.house_count)

        print('Build user co-rated house matrix ...')
        for house, users in house_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1
        print('Build user co-rated house matrix success!')

        # 计算相似性
        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
        print('Calculate user similarity matrix success!')
        print(self.user_sim_matrix)
    # 针对目标用户U，找到其最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_house
        rank = {}
        #print(user)
        watched_house = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for house in self.trainSet[v]:
                if house in watched_house:
                    continue
                rank.setdefault(house, 0)
                rank[house] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print("Evaluation start ...")
        N = self.n_rec_house
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_house = set()

        for i, user, in enumerate(self.trainSet):
            test_house = self.testSet.get(user, {})
            rec_house = self.recommend(user)
            for house, w in rec_house:
                if house in test_house:
                    hit += 1
                all_rec_house.add(house)
            rec_count += N
            test_count += len(test_house)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_house) / (1.0 * self.house_count)
        print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (precision, recall, coverage))


if __name__ == '__main__':
    rating_file = 'ratings.csv'
    userCF = UserBasedCF()
    userCF.get_dataset(rating_file)
    userCF.calc_user_sim()
    #userCF.evaluate()
    print(userCF.recommend('ldq8'))
