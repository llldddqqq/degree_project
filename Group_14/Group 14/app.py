from flask import Flask, request, redirect, render_template, session, url_for, flash
import Search
# from pymysql import *
import time
from db_process import *
import Usercf_house

app = Flask(__name__)
app.config["SECRET_KEY"] = 'abcde'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form.get('query'):
        query = request.form['query']
        return redirect(url_for('search', query=query))
    return render_template('home-7.html')

@app.route('/index_login/<user>', methods=['POST', 'GET'])
def index_login(user):
    if request.method == 'POST' and request.form.get('query'):
        query = request.form['query']
        return redirect(url_for('search', query=query))
    return render_template('home-7_login.html', username=user, featured=recommend_to_user(user))

@app.route('/blog')
def appointment_success():
    session['currentPage'] = 'blog'
    return render_template('blog.html')


@app.route('/login', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    #    if request.method=='GET':
    #       return render_template('login.html')
    user = request.form.get('username')
    pwd = request.form.get('password')
    if not check_in(user):
        return redirect('/signup')
    else:
        if db_user_login(user, pwd):
            session['CUS'] = user
            print('success')
            print(session.get('CUS'))
            return redirect(url_for('index_login', user=user))
        else:
            print('fail')
            return render_template('login.html', msg='wrong password')


@app.route('/signup', methods=['GET', "POST"])
def signup():
    #   if request.method=='GET':
    #       return render_template('login.html')
    user = request.form.get('username')
    pwd = request.form.get('password')
    # print(user)
    # print(pwd)
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


@app.route('/myprofile', methods=['GET', "POST"])
def myprofile():
    username = session.get('CUS')
    user = get_user_info(username)
    return render_template('my-profile.html', username=username, user=user)

@app.route('/editprofile', methods=['GET', "POST"])
def editprofile():
    username = session.get('CUS')
    user = get_user_info(username)
    return render_template('my-profile-edit.html', username=username, user=user)


@app.route('/check', methods=['GET', "POST"])
def check():
    username = session.get('CUS')
    user = get_user_info(username)
    return render_template('check-password.html', username=username, user=user)

@app.route('/checkpassword', methods=['GET', "POST"])
def checkpassword():
    username = session.get('CUS')
    user = get_user_info(username)
    alert="wrong"
    if user['user_password'] == request.form.get('password'):
        return render_template('change-password.html', username=username, user=user)
    else:
        return render_template('check-password.html', username=username, user=user, alert=alert)



@app.route('/changepassword', methods=['GET', "POST"])
def changepassword():
    username = session.get('CUS')
    alert = "wrong"
    if request.form.get('password1') == request.form.get('password2'):
        password=request.form.get('password1')
        update_user_password(username, password)
        return redirect(url_for('myprofile'))
    else:
        return render_template('change-password.html', username=username, alert=alert)

@app.route('/edit', methods=['GET', "POST"])
def edit():
    username = session.get('CUS')
    email = request.form.get('email')
    phone= request.form.get('phone')
    address = request.form.get('address')
    city = request.form.get('city')
    country = request.form.get('country')
    update_user_email(username, email)
    update_user_phone(username, phone)
    update_user_address(username, address)
    update_user_city(username, city)
    update_user_country(username, country)
    user = get_user_info(username)
    return redirect(url_for('myprofile'))


@app.route('/listings', methods=['GET', "POST"])
def listings():
    return render_template('grid-layout-4.html')


@app.route('/myproperty', methods=['GET', "POST"])
def myproperty():
    return render_template('my-property.html')


@app.route('/bookmarkproperty', methods=['GET', "POST"])
def bookmarkproperty():
    if session.get('CUS'):
        username = session.get('CUS')
        results = check_prefer(session.get('CUS'))
        house = []
        for r in results:
            house.append(get_house(r))
    return render_template('bookmark-list.html', house=house, username=username)


@app.route('/contacts', methods=['GET', "POST"])
def contacts():
    return render_template('contact.html')


@app.route('/estates/<id>', methods=['GET', "POST"])
def estatesdetail(id):
    house = get_house(id)
    if request.method == 'POST' and session.get('CUS'):
        add_prefer(session.get('CUS'), id)
    comments=read_comment(id)
    number='No'
    username=session.get('CUS')
    if comments:
        number=len(comments)
    return render_template('single-property-1.html', username=username, house=house, id=id, comments=comments, number=number)

@app.route('/comments/<id>', methods=['GET', "POST"])
def addcomment(id):
    if not session.get('CUS') is None:
        comment=request.form.get("comment")
        #comment = request.form["comment"]
        #print(comment)
        add_comment(session.get('CUS'), id, comment)
    return redirect(url_for('estatesdetail', id=id))


@app.route('/search/<query>', methods=['GET', "POST"])
def search(query):
    start_search = time.time()
    result = house_search(query)
    end_search = time.time()
    print('search time:', str(end_search - start_search))
    if request.method == 'POST':
        ptype = request.form.get('ptype')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        if ptype != '' or bedrooms != '' or bathrooms != '':
            for id in list(result):
                if ptype != '' and result[id]['type'] != ptype:
                    del result[id]
            for id in list(result):
                if bedrooms != '' and result[id]['bedroom_amount'] != int(bedrooms):
                    del result[id]
            for id in list(result):
                if bathrooms != '' and result[id]['bathroom_amount'] != int(bathrooms):
                    del result[id]
    return render_template('search.html', result=result)


@app.route('/logout')
def logout():
    if session.get('CUS'):
        session.pop('CUS')
    return redirect(url_for('index'))


def recommend_to_user(user):
    # 获取user信息
    house_list = Usercf_house.recommendation(user)
    # print(house_list)
    house_info = {}
    for i in house_list:
        house_info[i] = get_house(str(i))
    return house_info


# recommend_to_user('ldq')


if __name__ == '__main__':
    # print(recommend_to_user('ldq'))
    app.run()
