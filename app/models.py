from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    is_authenticated = True  # 判断用户是否登陆

    is_active = True

    is_anonymous = True

    @property
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    title = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self,title,body,user_id):
        self.title = title
        self.body = body
        self.user_id = user_id
    def __repr__(self):
        return '<Post %r>' % (self.title)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    IP = db.Column(db.String(32))
    ways = db.Column(db.String(100))
    request_method = db.Column(db.String(32))
    data_i = db.Column(db.String(32))
    data = db.Column(db.String(250))
    check = db.Column(db.String(100))
    is_do = db.Column(db.String(32))
    is_base = db.Column(db.String(32))
    is_base_do = db.Column(db.String(32))
    def __init__(self,name='1',IP='1',ways=1,request_method='1',data_i='1',data='1',check='1',is_do='1',is_base='1',is_base_do='1'):
        self.name = name
        self.IP = IP
        self.ways = ways
        self.request_method = request_method
        self.data_i = data_i
        self.data = data
        self.check = check
        self.is_do = is_do
        self.is_base = is_base
        self.is_base_do = is_base_do

    def __repr__(self):
        return '<Case %r>' % (self.name)