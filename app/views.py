from app import app, db, oid, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User,Module,Case,Project
from .test import request_cases,write_report
from .test import get_report
import json, time

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
            org_id = db.session.query(Project.id).filter_by(project_name=org_name).first()[0]
            module_id = db.session.query(Module.id).filter_by(module_name=module_name).first()[0]
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

@app.route('/editor', methods=['GET', 'POST'])
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
            org_name = request.form['project_name1']
            module_name = request.form['module_name1']
            org_id = db.session.query(Project.id).filter_by(project_name=org_name).first()[0]
            module_id = db.session.query(Module.id).filter_by(module_name=module_name).first()[0]
            Case.query.filter_by(id=id_num).update({Case.name:name,
                                                    Case.IP:server,
                                                    Case.ways:ways,
                                                    Case.request_method:request_method,
                                                    Case.data_i:data_i,
                                                    Case.data:data,
                                                    Case.check:check,
                                                    Case.is_base:is_base,
                                                    Case.org_id:org_id,
                                                    Case.module_id:module_id})
            db.session.commit()
            flash('用例更新成功')
            return redirect(url_for('case'))

@app.route('/do_case', methods=['GET', 'POST'])
def do_case():
    if request.method == 'POST':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            cases = Case.query.all()
            modules = Module.query.all()
            projects = Project.query.all()
            p_name = db.session.query(Project.project_name)
            m_name = db.session.query(Module.module_name)
            id_num = request.form['num2']
            case_name = request.form['names2']
            server = request.form['server2']
            way = request.form['way2']
            request_method = request.form['request_method2']
            data_type = request.form['data_i2']
            data_i = request.form['data2']
            check = request.form['check2']
            is_base = request.form['is_base2']
            org_name = request.form['project_name2']
            module_name = request.form['module_name2']
            start_time = time.strftime('%H:%M:%S')
            code = request_cases.get_cases(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base)
            end_time = time.strftime('%H:%M:%S')
            print('调试---用例:%s  响应结果：%d' % (case_name, code))
            result = {
                'org_name':org_name,
                'module_name':module_name,
                'code':code,
                'case_name':case_name,
                'start_time':start_time,
                'end_time':end_time,
            }
            return render_template('tiaoshi_result.html',
                                   cases=cases,
                                   modules=modules,
                                   projects=projects,
                                   p_name=p_name,
                                   m_name=m_name,
                                   title='用例',
                                   result=result
                                   )

@app.route('/do_many_case', methods=['GET', 'POST'])
def do_many_case():
    results = []
    succ_num = 0
    fail_num = 0
    start_time = time.strftime('%Y-%m-%d %H:%M:%S')
    if request.method =='GET':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            dics = request.args.to_dict()
            for dic in dics:
                json_d = json.loads(dic)
                num = json_d.get('len')
                for i in range(num):
                    k = str(i)
                    case_data = json_d.get(k)
                    id_num = case_data.get('id_num')
                    case_name = case_data.get('case_name')
                    server = case_data.get('server')
                    way = case_data.get('way')
                    request_method = case_data.get('request_method')
                    data_type = case_data.get('data_type')
                    data_i = case_data.get('data_i')
                    check = case_data.get('check')
                    is_base = case_data.get('is_base')
                    result_case, text, code = request_cases.get_cases(id_num, case_name, server, way, request_method, data_type, data_i, check, is_base)
                    result = [id_num, case_name, result_case, text, code]
                    results.append(result)
                    if result_case == 'success':
                        succ_num += 1
                    else:
                        fail_num += 1
    print('开始时间%s'%start_time)
    num = succ_num + fail_num
    end_time = time.strftime('%Y-%m-%d %H:%M:%S')
    write = write_report.Write_report(results,start_time,end_time,num,succ_num,fail_num)
    write.run_tem()
    print('测试报告写入完成')
    return 'ok'

@app.route('/selected_top_case', methods=['GET','POST'])
def selected_top_case():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        p_name = db.session.query(Project.project_name)
        m_name = db.session.query(Module.module_name)
        projects = Project.query.all()
        modules = Module.query.all()
        module_name_case = request.form['module_name_case']
        if module_name_case == '全部':
            cases = Case.query.all()
        else:
            case_id = db.session.query(Module.id).filter_by(module_name=module_name_case).first()[0]
            cases = Case.query.filter_by(module_id=case_id).all()
        return render_template("testcase.html",
                               cases=cases,
                               modules=modules,
                               projects=projects,
                               p_name=p_name,
                               m_name=m_name,
                               title='用例-' + module_name_case)

@app.route('/case')
def case():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        cases = Case.query.all()
        modules = Module.query.all()
        projects = Project.query.all()
        p_name = db.session.query(Project.project_name)
        m_name = db.session.query(Module.module_name)
        return render_template("testcase.html",
                               cases=cases,
                               modules=modules,
                               projects=projects,
                               p_name=p_name,
                               m_name=m_name,
                               title='用例')

@app.route('/project_module', methods=['GET', 'POST'])
def project_module():
    if request.method =='POST':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            projects = Project.query.all()
            project_name = request.form['project']
            if project_name == '全部':
                modules = Module.query.all()
            else:
                project_id = db.session.query(Project.id).filter_by(project_name=project_name).first()[0]
                modules = Module.query.filter_by(org_id=project_id).all()
            return render_template('module.html',
                                   projects=projects,
                                   modules=modules,
                                   title='模块-' + project_name)

@app.route('/module')
def module():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        projects = Project.query.all()
        modules = Module.query.all()
        return render_template("module.html",
                               projects=projects,
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

@app.route('/project')
def project():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        projects = Project.query.all()
        return render_template("project.html",
                               projects=projects,
                               title='项目')

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method =='POST':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            project_name = request.form['project_name']
            creator = request.form['creator']
            category = Project(project_name,creator)
            db.session.add(category)
            db.session.commit()
            flash('项目保存成功')
            return redirect(url_for('project'))

@app.route('/editor_project', methods=['GET', 'POST'])
def editor_project():
    if request.method =='POST':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            id_num = request.form['num1']
            project_name = request.form['project_name1']
            creator = request.form['creator1']
            Project.query.filter_by(id=id_num).update({Project.project_name: project_name,
                                                           Project.creator: creator})
            db.session.commit()
            flash('项目更新成功')
            return redirect(url_for('project'))

@app.route('/delete_project', methods=['GET', 'POST'])
def delete_project():
    if request.method =='GET':
        if not session.get('logged_in'):
            return redirect('login')
        else:
            ids = request.args.get('id')
            id = int(ids)
            Project.query.filter_by(id=id).delete()
            db.session.commit()
            flash('删除完成')
            return redirect(url_for('project'))

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
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        passwd = User.query.filter_by(password=password).first()

        if user is None:
            error = '无效账号'
        elif passwd is None:
            error = '无效密码'
        else:
            session['logged_in'] = True
            flash('登录成功')
            return redirect(url_for('index'))
    return render_template('login.html',
                           title='登录',
                           error=error,
                           form=LoginForm())

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/report')
def report():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        reports = get_report.get_report()
        return render_template("report.html",
                               reports=reports,
                               title='测试报告')

@app.route('/report_result')
def report_result():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        reports = get_report.get_report()
        for report in reports:
            return render_template("report/"+report,
                               title='测试报告')
