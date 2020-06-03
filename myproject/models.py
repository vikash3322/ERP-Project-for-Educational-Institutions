from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), default='default_profile.png')
    email = db.Column(db.String(64),  unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(64), index=True)
    roles = db.relationship('Role', secondary='user_roles')
    s_user = db.relationship('Students', backref='students', uselist=False)
    t_user = db.relationship('Teachers', backref='teachers', uselist=False)
    posts = db.relationship('BlogPost', backref='author', lazy=True)
   
    def __init__(self, email, username, password, user_type):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.user_type = user_type
        

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)


# Define the Role data-model

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    # Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id=user_id
        self.role_id=role_id

class Students(db.Model):

    __tablename__ = 'student'

    
    usn = db.Column(db.String(40), primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(140))
    last_name = db.Column(db.String(140))
    address = db.Column(db.String(240))
    branch = db.Column(db.String(140), db.ForeignKey('branch.branch_id'), nullable=False)
    sem = db.Column(db.String(140))
    sec = db.Column(db.String(140))
    attend = db.relationship('Attendances', backref='attendances', foreign_keys='Attendances.usn')
    s_users = db.relationship('User', backref='students', uselist=False)

   
    

    def __init__(self, usn, first_name, last_name, branch, sem, sec, address,  user_id):
        self.usn = usn
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.branch = branch
        self.sem = sem
        self.sec = sec
        self.user_id = user_id


class Teachers(db.Model):
    __tablename__ = 'teacher'

    t_id = db.Column(db.String(40), primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(140))
    last_name = db.Column(db.String(140))
    branch = db.Column(db.String(140))
    address = db.Column(db.String(240))
    

    def __init__(self, t_id, first_name, last_name, address, branch, user_id):
        self.t_id = t_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.branch = branch
        self.user_id = user_id


class Branchs(db.Model):

    __tablename__ = 'branch'

    branch_id = db.Column(db.String(40), primary_key=True, unique=True)
    branch_name = db.Column(db.String(140))
    sem = db.Column(db.Integer())
    sub = db.relationship('Subjects', backref='subject', lazy='dynamic')
    student = db.relationship('Students', backref='student', foreign_keys='Students.branch')


    def __init__(self, branch_id ,branch_name, sem):
        self.branch_id = branch_id
        self.sem = sem
        self.branch_name = branch_name

class Subjects(db.Model):

    __tablename__ = 'subject'

    sub_id = db.Column(db.String(40), primary_key=True, unique=True)
    sub_name = db.Column(db.String(140))
    sem = db.Column(db.Integer())
    branch = db.Column(db.String(140), db.ForeignKey('branch.branch_id', ondelete='CASCADE'), nullable=False)
    sub_atten = db.relationship('Attendances', backref='attends', lazy='dynamic')

    def __init__(self , sub_id, sub_name, sem, branch):
        self.sub_id = sub_id
        self.sub_name = sub_name
        self.sem = sem
        self.branch = branch


class Attendances(db.Model):

    __tablename__='attendance'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(60), nullable=False)
    attendance = db.Column(db.String(60))
    subject = db.Column(db.String(140), db.ForeignKey('subject.sub_id', ondelete='CASCADE'), nullable=False)
    usn = db.Column(db.String(140), db.ForeignKey('student.usn'), nullable=False)


    def __init__(self, date, subject, usn, attendance):
        self.date = date
        self.subject = subject
        self.attendance = attendance
        self.usn = usn
     
 
class BlogPost(db.Model):
    # Setup the relationship to the User table
    users = db.relationship(User)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    blog_img = db.Column(db.String(20), default='default_img.png')
    title = db.Column(db.String(140), nullable=False)
    topic = db.Column(db.String(60), nullable=False)
    text = db.Column(db.Text, nullable=False)
    blogcount = db.relationship('Blogcount', backref='coupos')
    usr = db.relationship('User', backref='userspost')
    
    def __init__(self, title, text, topic, blog_img, user_id):
        self.title = title
        self.text = text
        self.topic = topic
        self.blog_img = blog_img
        self.user_id = user_id

    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"


class Blogcount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)
    click = db.Column(db.Integer, nullable=False)
    blogs = db.relationship('BlogPost', backref='countpost')

    def __init__(self, blog_id, click):
        self.blog_id = blog_id
        self.click = click

class TimeTables(db.Model):

    __tablename__ ='timetable'

    id = db.Column(db.Integer, primary_key=True)
    val1 = db.Column(db.String(120))
    val2 = db.Column(db.String(120))
    val3 = db.Column(db.String(120))
    val4 = db.Column(db.String(120))
    val5 = db.Column(db.String(120))
    val6 = db.Column(db.String(120))
    val7 = db.Column(db.String(120))
    val8 = db.Column(db.String(140))
    val9 = db.Column(db.String(140))
    val10 = db.Column(db.String(140))
    val11 = db.Column(db.String(140))
    val12 = db.Column(db.String(140))
    val13 = db.Column(db.String(140))
    val14 = db.Column(db.String(140))
    val15 = db.Column(db.String(140))
    val16 = db.Column(db.String(140))
    val17 = db.Column(db.String(140))
    val18 = db.Column(db.String(140))
    val19 = db.Column(db.String(140))
    val20 = db.Column(db.String(140))
    val21 = db.Column(db.String(140))
    val22 = db.Column(db.String(140))
    val23 = db.Column(db.String(140))
    val24 = db.Column(db.String(140))
    val25 = db.Column(db.String(140))
    val26 = db.Column(db.String(140))
    val27 = db.Column(db.String(140))
    val28 = db.Column(db.String(140))
    val29 = db.Column(db.String(140))
    val30 = db.Column(db.String(140))
    val31 = db.Column(db.String(140))
    val32 = db.Column(db.String(140))
    val33 = db.Column(db.String(140))
    val34 = db.Column(db.String(140))
    val35 = db.Column(db.String(140))
    branch = db.Column(db.String(140))
    sem = db.Column(db.String(140))
    sec = db.Column(db.String(140))

    def __init__(self, val1, val2, val3, val4,  val5, val6, val7, val8, val9, val10, val11, val12, val13, val14, val15, val16, val17, val18, val19, val20, val21, val22, val23, val24, val25, val26, val27, val28, val29, val30, val31, val32, val33, val34, val35, branch, sem , sec):
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3
        self.val4 = val4
        self.val5 = val5
        self.val6 = val6
        self.val7 = val7
        self.val8 = val8
        self.val9 = val9
        self.val10 = val10
        self.val11 = val11
        self.val12 = val12
        self.val13 = val13
        self.val14 = val14
        self.val15 = val15
        self.val16 = val16
        self.val17 = val17
        self.val18 = val18
        self.val19 = val19
        self.val20 = val20
        self.val21 = val21
        self.val22 = val22
        self.val23 = val23
        self.val24 = val24
        self.val25 = val25
        self.val26 = val26
        self.val27 = val27
        self.val28 = val28
        self.val29 = val29
        self.val30 = val30
        self.val31 = val31
        self.val32 = val32
        self.val33 = val33
        self.val34 = val34
        self.val35 = val35
        self.branch = branch
        self.sem = sem
        self.sec = sec


class Classroompost(db.Model):
    # Setup the relationship to the User table
    users = db.relationship(User)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, topic, user_id):
        self.title = title
        self.text = text
        self.topic = topic
        self.user_id = user_id
