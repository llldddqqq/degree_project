from pymysql import *
from Search import search
import sys
import Usercf_house
sys.setrecursionlimit(10000000)


def check_in(user):
    host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
    port = 3306
    db_user = 'dingqi'
    db_password = 'Liu18501303736'
    database = 'degree_project_db'
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select user_name from user_info Where user_name='" + str(user) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # print(result)
    if result == '' or len(result) == 0:
        return False
    if result[0][0] == user:
        return True
    else:
        return False


# print(check_in('ldq'))

def db_user_login(user, password):
    host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
    port = 3306
    db_user = 'dingqi'
    db_password = 'Liu18501303736'
    database = 'degree_project_db'
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select user_password from user_info Where user_name='" + user + "'"
    cur.execute(sql)
    result = cur.fetchall()
    if not check_in(user):
        return 'you need to signup first'
    if result[0][0] == password:
        return True
    else:
        return False


# db_user_check('ldq','liu1')
def db_user_signup(user, password):
    print(user, password)
    host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
    port = 3306
    db_user = 'dingqi'
    db_password = 'Liu18501303736'
    database = 'degree_project_db'
    if check_in(user):
        return False
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "insert into user_info(user_name,user_password,saved_property) VALUE (" + "'" + str(user) + "'," + "'" + str(
        password) + "'," + "'" + '' + "'" + ")"
    cur.execute(sql)
    conn.commit()
    cur.close()
    print(user, password)
    return True


# for i in range(30):
#     string = 'ldq' + str(i)
#     db_user_signup(string, 'liu1',str(i))


def house_search(query):
    host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
    port = 3306
    db_user = 'dingqi'
    db_password = 'Liu18501303736'
    database = 'degree_project_db'
    results = search(query)
    # print(results)
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    house_dic = {}
    for id in results:
        temp = {}
        sql = "select * from datas Where id='" + str(id) + "'"
        cur.execute(sql)
        result = cur.fetchall()
        temp['address'] = result[0][1]
        temp['postcode'] = result[0][2]
        temp['county'] = result[0][3]
        temp['price'] = result[0][4]
        temp['full market price'] = result[0][5]
        temp['vat_incude'] = result[0][6]
        temp['type'] = result[0][7]
        temp['square'] = result[0][8]
        temp['pic_add'] = result[0][9]
        house_dic[id] = temp
    return house_dic


# a=house_search('Dublin')
# print(a)

def add_prefer(username, house_id):
    host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
    port = 3306
    db_user = 'dingqi'
    db_password = 'Liu18501303736'
    database = 'degree_project_db'
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET saved_property = CONCAT(saved_property,'" + str(
        house_id) + ",'" + ") WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()


def get_house(id):
    host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
    port = 3306
    db_user = 'dingqi'
    db_password = 'Liu18501303736'
    database = 'degree_project_db'
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select * from datas Where id='" + str(id) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    #print(result)
    house_dic = {}
    head = ['id','address',
            'postcode',
            'country',
            'price',
            'full_market_price',
            'vat_exclusive',
            'description',
            'size',
            'pic_address',
            'message',
            'bedroom_amount',
            'bathroom_amount',
            'house_orientation'
            ]
    for i in range(0,len(head)):
        house_dic[head[i]]=result[0][i]
    return house_dic
#print(get_house('1'))

#add_prefer('ldqwww', 23521)
