from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

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


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    IP = db.Column(db.String(32))
    ways = db.Column(db.String(100))
    request_method = db.Column(db.String(32))
    data_i = db.Column(db.String(32))
    data = db.Column(db.String(250))
    check = db.Column(db.String(100))
    is_base = db.Column(db.String(32))
    org_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)
    is_succ = db.Column(db.Integer)

    def __init__(self,name,IP,ways,request_method,data_i,data,check,is_base,org_id,module_id,is_succ):
        self.name = name
        self.IP = IP
        self.ways = ways
        self.request_method = request_method
        self.data_i = data_i
        self.data = data
        self.check = check
        self.is_base = is_base
        self.org_id = org_id
        self.module_id = module_id
        self.is_succ = is_succ

    def __repr__(self):
        return '<Case %r>' % (self.name)

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(32))
    creator = db.Column(db.String(32))
    org_id = db.Column(db.Integer)

    def __init__(self,module_name,creator,org_id):
        self.module_name = module_name
        self.creator = creator
        self.org_id = org_id

    def __repr__(self):
        return '<Module %r>' % (self.module_name)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(32))
    creator = db.Column(db.String(32))

    def __init__(self,project_name,creator):
        self.project_name = project_name
        self.creator = creator

    def __repr__(self):
        return '<Project %r>' % (self.project_name)