from pymysql import *


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
    #print(result)
    if result =='' or len(result)==0:
        return False
    if result[0][0] == user:
        return True
    else:
        return False
#print(check_in('ldq'))

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
    sql = "insert into user_info(user_name,user_password) VALUE (" + "'" + str(user) + "'," + "'" + str(password) + "')"
    cur.execute(sql)
    conn.commit()
    cur.close()
    print(user, password)
    return True
# db_user_signup('ldq','liu1')
