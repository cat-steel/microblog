from app import app, db, oid, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User,Module,Case,Project

@app.before_request
def before_request():
    g.user = current_user

@app.route('/add_testcase', methods=['GET', 'POST'])
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
            is_base = request.form['is_base']
            org_name = request.form['project_name']
            module_name = request.form['model_name']
            if org_name == '人员系统':
                org_id = 1
            else:
                org_id = 2
            if module_name == '从业人员管理':
                module_id = 1
            else:
                module_id = 2
            category = Case(name,server,ways,request_method,data_i,data,check,is_base,org_id,module_id)
            db.session.add(category)
            db.session.commit()
            flash('用例保存成功')
            return redirect(url_for('case'))

@app.route('/delete_case', methods=['GET', 'POST'])
def delete_case():
    if request.method =='GET':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            ids = request.args.get('id')
            id = int(ids)
            print('id:%s'%id)
            Case.query.filter_by(id=id).delete()
            print('删除成功')
            db.session.commit()
            flash('删除完成')
            return redirect(url_for('case'))

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
            Case.query.filter_by(id=id_num).update({Case.name:name,
                                              Case.IP:server,
                                              Case.ways:ways,
                                              Case.request_method:request_method,
                                              Case.data_i:data_i,
                                              Case.data:data,
                                              Case.check:check,
                                              Case.is_base:is_base})
            db.session.commit()
            flash('用例更新成功')
            return redirect(url_for('case'))

@app.route('/case')
def case():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        cases = Case.query.all()
        return render_template("testcase.html",
                               cases=cases,
                               title='用例')

@app.route('/module')
def module():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        modules = Module.query.all()
        return render_template("module.html",
                               modules=modules,
                               title='模块')

@app.route('/add_module', methods=['GET', 'POST'])
def add_module():
    if request.method =='POST':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            org_name = request.form['project_name']
            module_name = request.form['module_name']
            creator = request.form['creator']
            if org_name == '人员系统':
                org_id = 1
            else:
                org_id = 2
            category = Module(module_name,creator,org_id)
            db.session.add(category)
            db.session.commit()
            flash('模块保存成功')
            return redirect(url_for('module'))

@app.route('/editor_module', methods=['GET', 'POST'])
def editor_module():
    if request.method =='POST':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            id_num = request.form['num1']
            org_name = request.form['project_name1']
            module_name = request.form['module_name1']
            creator = request.form['creator1']
            if org_name == '人员系统':
                org_id = 1
            else:
                org_id = 2
            Module.query.filter_by(id=id_num).update({Module.module_name: module_name,
                                                    Module.creator: creator,
                                                    Module.org_id: org_id})
            db.session.commit()
            flash('模块更新成功')
            return redirect(url_for('module'))

@app.route('/delete_module', methods=['GET', 'POST'])
def delete_module():
    if request.method =='GET':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            ids = request.args.get('id')
            id = int(ids)
            Module.query.filter_by(id=id).delete()
            db.session.commit()
            flash('删除完成')
            return redirect(url_for('module'))

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        return render_template("index.html",
                               title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        print(username)
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        print('user:%s'%user)
        passwd = User.query.filter_by(password=password).first()

        if user is None:
            error = 'Invalid username'
        elif passwd is None:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html',
                           title='登录',
                           error=error,
                           form=LoginForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
