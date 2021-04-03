import csv

from pymysql import *

import porter

csv_file = csv.reader(open('PPR-ALL.csv', encoding='gbk'))
house_info = {}
house_index_info = {}

punc = [',', '/', '.']
stemmer = porter.PorterStemmer()
i=1
error=0
for line in csv_file:
    line2 = line
    postcode=line2[2].replace("\\pP|\\pS|\n", "")
    country= line2[3].replace("\\pP|\\pS|\n", "")
    price=line2[4].replace("\\pP|\\pS|\n", "")
    not_full_price=line2[5].replace("\\pP|\\pS|\n", "")
    vat=line2[6].replace("\\pP|\\pS|\n", "")
    property_info= line2[7].replace("\\pP|\\pS|\n", "")
    size= line2[8].replace("\\pP|\\pS|\n", "")
    address=line2[1].replace("\\pP|\\pS|\n", "")
    host = 'rm-2ze6920m86z2g1by69o.mysql.rds.aliyuncs.com'
    port = 3306
    db_user = 'dingqi'
    db_password = 'Liu18501303736'
    database = 'degree_project_db'
    try:
        conn = connect(host=host, port=port, user=db_user, password=db_password, database=database)
        cur = conn.cursor()
        sql = "insert into datas(id,address,postcode,country,price,not_full_price,vat,property_info,size) VALUE (" +"'"+ str(i) +"'"+ "," + "'" + address + "',"+ "'"+postcode +"',"+"'"+country+\
              "','"+price+"','"+not_full_price+"','"+vat+"','"+property_info+"','"+size+"')"
        print(sql)
        i+=1
        cur.execute(sql)
        conn.commit()
        cur.close()
    except:
        error+=1
        print("error number",error)
        continue
#print(house_info) datas(id,address,postcode,country,price,not_full_price,vat,property_info,size)
