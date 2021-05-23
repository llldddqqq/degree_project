import Usercf_house
from pymysql import *

host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
port = 3306
db_user = 'dingqi'
db_password = 'Liu18501303736'
database = 'degree_project_db'


def recommend_to_user(user):
    # 获取user信息
    house_list = Usercf_house.recommendation(user)
    house_list2 = [1002, 1203, 12402, 3254, 234, 1, 23, 124, 12535, 4234]
    pivot = 10 - len(house_list) - 1
    if len(house_list) < 10:
        for i in range(0, pivot+1):
            house_list.append(house_list2[i])
    return house_list


#print(recommend_to_user('ldq'))
def to_string(list):
    str1=''
    for i in list:
        str1=str1+str(i)+","
    return str1[:-1]


def get_all_user():
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select user_name from user_info"
    cur.execute(sql)
    result = cur.fetchall()
    users = []
    for i in result:
        users.append(i[0])
    return users


def update():
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    users = get_all_user()
    for user in users:
        try:
            result=to_string(recommend_to_user(user))
            sql="UPDATE user_info SET recom='"+result+"'"+"WHERE user_name='"+user+"'"
            cur.execute(sql)
            conn.commit()
        except:
            result2='1,3,7,10,12,13,14,15,16,17'
            sql = "UPDATE user_info SET recom='" + result2 + "'"+"WHERE user_name='"+user+"'"
            cur.execute(sql)
            conn.commit()
    cur.close()

update()
