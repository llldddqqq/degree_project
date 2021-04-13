from flask import Flask, request, redirect, render_template, session, url_for, flash
import Search
from pymysql import *
import time
from db_process import *
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form.get('query'):
        query = request.form['query']
        return redirect(url_for('search', query=query))
    return render_template('home-7.html')

@app.route('/blog')
def appointment_success():
    session['currentPage'] = 'blog'
    return render_template('blog.html')

@app.route('/login',methods=['GET',"POST"])#路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
#    if request.method=='GET':
 #       return render_template('login.html')
    user=request.form.get('username')
    pwd=request.form.get('password')
    if not check_in(user):
        return redirect('/signup')
    else:
        if db_user_login(user, pwd):
            print('success')
            return render_template('my-profile.html')
        else:
            print('fail')
            return render_template('login.html', msg='wrong password')




@app.route('/signup',methods=['GET',"POST"])
def signup():
 #   if request.method=='GET':
 #       return render_template('login.html')
    user=request.form.get('username')
    pwd=request.form.get('password')
    print(user)
    print(pwd)
    if check_in(user):
        flash('This user has been registered')
        return redirect('/login')
    else:
        if db_user_signup(user, pwd):
            flash('sign up success')
            return redirect('/')
        else:
            flash('sign up failed')
            return redirect('/')

@app.route('/search/<query>',methods=['GET',"POST"])
def search(query):
    start_search = time.time()
    result = house_search(query)
    end_search = time.time()
    print('search time:', str(end_search - start_search))
    return render_template('search.html', result=result)


def recommend_to_user(user):
    #获取user信息
    house_list=Usercf_house.recommendation(user)
    #print(house_list)
    house_info={}
    for i in house_list:
        house_info[i]=get_house(str(i))
    return house_info
#recommend_to_user('ldq')
if __name__ == '__main__':
    #(recommend_to_user('ldq'))
    app.run()
