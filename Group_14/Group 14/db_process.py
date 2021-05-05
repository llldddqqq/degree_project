from pymysql import *
from Search import search
import sys
import Usercf_house
import json

sys.setrecursionlimit(10000000)
host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
port = 3306
db_user = 'dingqi'
db_password = 'Liu18501303736'
database = 'degree_project_db'


def check_in(user):
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
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET saved_property = CONCAT(saved_property,'" + str(
        house_id) + ",'" + ") WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()


def check_prefer(username):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql2 = "select saved_property from user_info where user_name='" + username + "'"
    cur.execute(sql2)
    result = cur.fetchall()
    results = result[0][0].split(',')
    return results


def get_house(id):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select * from datas Where id='" + str(id) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    # print(result)
    house_dic = {}
    head = ['id', 'address',
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
            'house_orientation',
            'sold'
            ]
    for i in range(0, len(head)):
        house_dic[head[i]] = result[0][i]
    return house_dic


# print(get_house('2'))
# house = []
# result = ['1', '2', '3']
# for r in result:
#     house.append(get_house(r))
# for h in house:
#     print(h['address'])
# add_prefer('ldqwww', 23521)
def update_user_phone(username, phone):  # curr_address, city, country):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET pthone_number = '" + str(phone) + "'" + "WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()
    # print('success', phone)


# update_user_phone('ldq',18501303736)
def update_user_address(username, address):  # curr_address, city, country):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET curr_address = '" + str(address) + "'" + "WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()


def update_user_city(username, city):  # curr_address, city, country):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET city = '" + str(city) + "'" + "WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()


def update_user_country(username, country):  # curr_address, city, country):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET country = '" + str(country) + "'" + "WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()


def update_user_password(username, password):  # curr_address, city, country):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET user_password = '" + str(password) + "'" + "WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()


# def get_search_house():
#     conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
#     cur = conn.cursor()
#     sql = "SELECT * from" + ' search'
#     cur.execute(sql)
#     result = cur.fetchall()
#     cur.close()
#     house_dic = {}
#     for res in result:
#         house_temp = {}
#         house_temp['term'] = json.loads(res[2])
#         house_temp['indoclen'] = res[1]
#         house_dic['id'] = house_temp
#         print(house_temp)
#     # cur.close()
#     return house_dic

#/home/dingqi.liu/pictures/pics/1
def update_pic():
    err=0
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    for j in range(0,462186):
        # route = "/home/team/group14/pics/" + str((j+1)%212) + ".JPG"
        #print(route)
        sql = "UPDATE datas SET pic_address = '/home/team/group14/pics/" + str((j+1)%212) + ".JPG'" + " where id='" + str(j+1)+"'"
        #print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except:
            err+=1
            print(err)
    cur.close()
#update_pic()

def get_house_inprice(low,high):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select * from datas WHERE price>"+str(low)+" and price<"+str(high)
    print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    house_dic = {}
    head = ['id', 'address',
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
            'house_orientation',
            'sold'
            ]
    for i in range(0,len(result)):
        for j in range(0,len(head)):
            house_dic[j]=result[i][j]
    return house_dic
#print(get_house_inprice(100,50000))
def get_house_insize(low,high):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select * from datas WHERE size>="+str(low)+" and size<="+str(high)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    house_dic = {}
    head = ['id', 'address',
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
            'house_orientation',
            'sold'
            ]
    for i in range(0,len(result)):
        for j in range(0,len(head)):
            house_dic[j]=result[i][j]
    return house_dic
#print(get_house_insize(38,50))


def recomm_new(username):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    id='1,3,7,10,12,13,14,15,16,17'
    sql = "UPDATE user_info SET recom = '"+id+"'"+" WHERE user_name='"+ username+"'"
    #print(sql)
    cur.execute(sql)
    conn.commit()
    cur.close()
#recomm_new('ldq')

