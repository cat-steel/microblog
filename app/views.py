from app import app, db, oid, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User,Post,Case

@app.before_request
def before_request():
    g.user = current_user
    print(current_user)

@app.route('/add', methods=['GET', 'POST'])
def add_testcase():
    if request.method =='POST':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            name = request.form['names']
            server = request.form['server']
            ways = request.form['way']
            request_method = request.form['request_method']
            data_i = request.form['data_i']
            data = request.form['data']
            check = request.form['check']
            is_do = request.form['is_do']
            is_base = request.form['is_base']
            is_base_do = request.form['is_base_do']
            category = Case(name,server,ways,request_method,data_i,data,check,is_do,is_base,is_base_do)
            db.session.add(category)
            db.session.commit()
            flash('用例保存成功')
            return redirect(url_for('show'))

@app.route('/delete')
def delete():
    Case.query.filter_by(id=ids).delete()
    #print('ids:%s'%ids)
    #db.session.delete(ids)
    db.session.commit()
    return redirect(url_for('show'))
@app.route('/')
def show():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        cases = Case.query.all()
        print('categorys:%s'%cases)
        return render_template("testcase.html",
                               title='Home',
                               cases=cases)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        passwd = User.query.filter_by(password=password).first()

        if user is None:
            error = 'Invalid username'
        elif passwd is None:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            print('开始重定向转到主页')
            return redirect(url_for('show'))
    return render_template('login.html',
                           title='登录',
                           error=error,
                           form=LoginForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


