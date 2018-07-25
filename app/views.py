from app import app, db, oid, lm
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm
from .models import User,Post

@app.before_request
def before_request():
    g.user = current_user
    print(current_user)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        title = request.form['title']
        content = request.form['text']
        category = Post(title, content, 1001)
        db.session.add(category)
        db.session.commit()
        flash('新文章保存成功')
        return redirect(url_for('show'))
@app.route('/')
def show():
    if not session.get('logged_in'):
        return redirect('login')
    else:
        categorys = Post.query.all()
        print('categorys:%s'%categorys)
        return render_template("index.html",
                               title='Home',
                               entries=categorys)

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