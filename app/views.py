from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data +'",remenber_me=' + str(form.remenber_me))
        return redirect('/index')
    return render_template('login.html',
                           title='登录',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])