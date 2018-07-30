from app import app, db, oid, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User,Post,Case

@app.before_request
def before_request():
    g.user = current_user

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
            print('请求方式：%s' % request_method)
            data_i = request.form['data_i']
            data = request.form['data']
            check = request.form['check']
            is_base = request.form['is_base']
            is_base_do = request.form['is_base_do']
            category = Case(name,server,ways,request_method,data_i,data,check,'',is_base,is_base_do)
            db.session.add(category)
            db.session.commit()
            flash('用例保存成功')
            return redirect(url_for('show'))

@app.route('/delete/', methods=['GET', 'POST'])
def delete():
    if request.method =='GET':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            ids = request.args.get('id')
            id = int(ids)
            Case.query.filter_by(id=id).delete()
            db.session.commit()
            flash('删除完成')
            return redirect(url_for('show'))

@app.route('/editor/', methods=['GET', 'POST'])
def editor():
    if request.method == 'POST':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            id_num = request.form['num1']
            name = request.form['names1']
            server = request.form['server1']
            ways = request.form['way1']
            request_method = request.form['request_method1']
            data_i = request.form['data_i1']
            data = request.form['data1']
            check = request.form['check1']
            is_base = request.form['is_base1']
            is_base_do = request.form['is_base_do1']
            Case.query.filter_by(id=id_num).update({Case.name:name,
                                              Case.IP:server,
                                              Case.ways:ways,
                                              Case.request_method:request_method,
                                              Case.data_i:data_i,
                                              Case.data:data,
                                              Case.check:check,
                                              Case.is_do:'',
                                              Case.is_base:is_base,
                                              Case.is_base_do:is_base_do})
            db.session.commit()
            flash('用例更新成功')
            return redirect(url_for('show'))

@app.route('/case')
def case():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        cases = Case.query.all()
        return render_template("testcase.html",
                               cases=cases)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        cases = Case.query.all()
        return render_template("index.html",
                               title='Home')

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
            return redirect(url_for('show'))
    return render_template('login.html',
                           title='登录',
                           error=error,
                           form=LoginForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


