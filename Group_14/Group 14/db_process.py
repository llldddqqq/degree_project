from pymysql import *
from Search import search
import json

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
    print(sql)
    cur.execute(sql)
    #print(sql)
    conn.commit()
    cur.close()
    print(user, password)
    return True
#print('ldq','123')

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
        temp['bedroom_amount'] = result[0][11]
        temp['bathroom_amount'] = result[0][12]
        house_dic[id] = temp
    return house_dic


# a=house_search('Dublin')
# print(a)

def get_user_info(username):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select * from user_info Where user_name='" + str(username) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    head = ['user_name', 'user_password', 'saved_property', 'email', 'phone_number', 'curr_address', 'city', 'country',
            'recom']
    user_info = {}
    for i in range(0, len(result)):
        for j in range(0, len(head)):
            user_info[head[j]] = result[i][j]
    return user_info


# print(get_user_info('ldq'))


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
    results = result[0][0].split(',')[:-1]
    return results


def renew_prefer(username):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET saved_property ='' WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()


print(check_prefer('ldq0'))


def delete_prefer(username, house_id):
    prefers = check_prefer(username)
    if str(house_id) in prefers:
        prefers.remove(str(house_id))
        renew_prefer('ldq1')
    else:
        return False
    for house in prefers:
        add_prefer(username, house)
    return True


# print(delete_prefer('ldq1', 1))


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


def update_user_email(username, email):  # curr_address, city, country):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "UPDATE user_info SET email = '" + str(email) + "'" + "WHERE user_name ='" + username + "'"
    cur.execute(sql)
    conn.commit()
    cur.close()


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


# /home/dingqi.liu/pictures/pics/1
def update_pic():
    err = 0
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    for j in range(0, 462186):
        # route = "/home/team/group14/pics/" + str((j+1)%212) + ".JPG"
        # print(route)
        sql = "UPDATE datas SET pic_address = '/home/team/group14/pics/" + str(
            (j + 1) % 212) + ".JPG'" + " where id='" + str(j + 1) + "'"
        # print(sql)
        try:
            cur.execute(sql)
            conn.commit()
        except:
            err += 1
            print(err)
    cur.close()


# update_pic()

def get_house_inprice(low, high):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select * from datas WHERE price>" + str(low) + " and price<" + str(high)
    # print(sql)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    house_dic = {}
    head = ['address',
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
    # print(result[0][0], result[1][0])
    for i in range(0, len(result)):
        temp = {}
        for j in range(0, len(head)):
            temp[head[j]] = result[i][j + 1]
        house_dic[result[i][0]] = temp
    return house_dic


# print(get_house_inprice(100,50000))
def get_house_insize(low, high):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select * from datas WHERE size>=" + str(low) + " and size<=" + str(high)
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    house_dic = {}
    head = ['address',
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
    # print(result[0][0], result[1][0])
    for i in range(0, len(result)):
        temp = {}
        for j in range(0, len(head)):
            temp[head[j]] = result[i][j + 1]
        house_dic[result[i][0]] = temp
    return house_dic


# print(get_house_insize(38, 50))


def recomm_new(username):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    id = '1,3,7,10,12,13,14,15,16,17'
    sql = "UPDATE user_info SET recom = '" + id + "'" + " WHERE user_name='" + username + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    cur.close()


# recomm_new('ldq')
def check_recomm(username):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql2 = "select recom from user_info where user_name='" + username + "'"
    cur.execute(sql2)
    result = cur.fetchall()
    results = result[0][0].split(',')
    if result[0][0] is None or result[0][0] == '':
        return False
    return results
#print(check_recomm('123'))


def add_comment(username, house_id, comments):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    temp_dic = {}
    temp_dic[username] = comments
    str1 = json.dumps(temp_dic)
    sql = "UPDATE datas SET message = CONCAT(message,'" + str1 + ",'" + ") WHERE id ='" + str(house_id) + "'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    cur.close()


# add_comment('ldq', 1, 'such a 4')

def read_comment(house_id):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select message from datas WHERE id='" + str(house_id) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    if result[0][0] is None or result[0][0] == '':
        return False
    list1 = result[0][0][:-1].split(",")
    # print(len(list1))
    for i in range(0, len(list1)):
        list1[i] = json.loads(list1[i])
    # print(list1)
    return list1


def get_house_inoren(orientation):
    conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
    cur = conn.cursor()
    sql = "select * from datas WHERE house_orientation='" + str(orientation) + "'"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    house_dic = {}
    head = ['address',
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
    # print(result[0][0], result[1][0])
    for i in range(0, len(result)):
        temp = {}
        for j in range(0, len(head)):
            temp[head[j]] = result[i][j + 1]
        house_dic[result[i][0]] = temp
    return house_dic

# print(get_house_inoren('west'))

# def filter(house_dic,low_price,high_price,low_size,high_size,house_orien,bath_amount,bed_amount):
#     for house_id in house_dic:



