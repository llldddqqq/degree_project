from flask import Flask , request, redirect, render_template,session
from pymysql import *
from db_process import *
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def appointment_success():
    session['currentPage'] = 'blog'
    return render_template('blog.html')

@app.route('/login',methods=['GET',"POST"])#路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    if request.method=='GET':
        return render_template('login.html')
    user=request.form.get('user')
    pwd=request.form.get('pwd')
    if not check_in(user):
        return redirect('/signup')
    else:
        if db_user_login(user,pwd):
            return render_template('home-2.html')
        else:
            return render_template('login.html',msg='wrong password')



@app.route('/signup',methods=['GET',"POST"])
def signup():
    if request.method=='GET':
        return render_template('login.html')
    user=request.form.get('user')
    pwd=request.form.get('pwd')
    if check_in(user):
        return redirect('/index')
    else:
        if db_user_signup(user,pwd):
            return redirect('login.html')



if __name__ == '__main__':
    app.run()
