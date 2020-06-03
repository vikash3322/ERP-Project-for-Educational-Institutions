from myproject import app, db, login_manager, safe, mail, allowed_file
from flask import render_template, redirect, request, url_for, flash, abort, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from myproject.models import User, Students, Teachers,  Branchs, Subjects, Attendances, TimeTables, BlogPost, Blogcount
from myproject.forms import *
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from myproject.picture_handler import add_profile_pic
from sqlalchemy import or_, and_, func
import secrets
import os
from PIL import Image
import bleach
from werkzeug.utils import secure_filename


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load.""" 
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


def validate_on_submit(self):
    """
    Checks if form has been submitted and if so runs validate. This is
    a shortcut, equivalent to ``form.is_submitted() and form.validate()``
    """
    return self.is_submitted() and self.validate()

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    

    if current_user.is_authenticated:
        return redirect(url_for('index'))



    if request.method == 'POST':
       email = request.form['email']
       password1 = request.form['password']
       usertype = request.form['optradio']
       user = User.query.filter_by(email=email).first()
       
       
       if user.user_type == usertype and usertype == 'student':
           if user and user.check_password(password=password1):
               login_user(user)
               next_page = request.args.get('next')
               return redirect(next_page or url_for('student_info'))
       
       elif user.user_type == usertype and usertype == 'teacher':
           if user and user.check_password(password=password1):
               login_user(user)
               next_page = request.args.get('next')
               return redirect(next_page or url_for('teacher_info'))
       
       elif user.user_type == usertype and usertype == 'admin':
           if user and user.check_password(password=password1):
               login_user(user)
               next_page = request.args.get('next')
               return redirect(next_page or url_for('admin_dashboard'))
       else:
           flash('your user type opption is not correct')
       
    flash('Enter your login details')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['psw']
        rpsw = request.form['rpsw']
        usertype = request.form['optradio']
        if User.query.filter_by(email=email).first():
            flash('Email address already register')
            return render_template('register.html')
        
        elif User.query.filter_by(username=username).first():
            flash('username already taken')
            return render_template('register.html')


        elif password == rpsw:
             user = User(email=email, username=username, password=password, user_type=usertype)
             db.session.add(user)
             db.session.commit()
             flash('Thanks for registering! Now you can login!')
             return redirect(url_for('login'))
        else:
            flash('please enter same password')
            return render_template('register.html')
    return render_template('register.html')


##############################################################################################################
######################################## ADMIN SECTION #######################################################
##############################################################################################################

@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():

    if request.method == 'POST' and  'teach_search' in request.form:
        branch = request.form['branch']
        tid = request.form['t_id']
        teacher = Teachers.query.filter_by(branch=branch).all()
        if teacher != None:
            return render_template('admin/dashboard.html', teacher=teacher)
        
        else:
            teacher = Teachers.query.filter_by(t_id=tid).first()
            return render_template('admin/dashboard.html', teacher=teacher)

    

    if request.method == 'POST' and 'teach_submit' in request.form:
        email = request.form['email']
        password = request.form['psw']
        password1 = request.form['rpsw']
        usertype = request.form['usertype']
        username = request.form['username']

        if User.query.filter_by(email=email).first():
            flash('Email  address already register')
            return redirect(url_for('admin_dashboard'))
        
        elif User.query.filter_by(username=username).first():
            flash(' Username address already register')
            return redirect(url_for('admin_dashboard'))



        elif password == password1:
            teachers1 = User(email=email, username=username,password=password, user_type=usertype)
            db.session.add(teachers1)
            db.session.commit()
            flash('User successfully register')
            msg = Message("Confirm Email", sender="stufa@gmail.com", recipients=[email])
            msg.html = render_template('/mail/register.html', email=email, password=password, username=username)
            mail.send(msg)
            return redirect(url_for('admin_dashboard'))
        
        else:
            flash('Please enter same password')
            return redirect(url_for('admin_dashboard'))

    return render_template('admin/dashboard.html')


@app.route('/admin_branch', methods=['GET', 'POST'])
@login_required
def admin_branch():
    form = BranchForm()
    if form.validate_on_submit():
        branch = Branchs(branch_id=form.branch_id.data, branch_name=form.branch_name.data, sem=form.sem.data)
        db.session.add(branch)
        db.session.commit()
    
    branches = Branchs.query.order_by(Branchs.branch_name).all()
    return render_template('admin/branch.html',form=form, branches=branches)


@app.route('/admin_subject', methods=['GET', 'POST'])
@login_required
def admin_subject():
    if request.method == 'POST':
        sub_id = request.form['sub_id']
        sub_name = request.form['sub_name']
        branch = request.form['branch']
        sem = request.form['sem']

        subject = Subjects(sub_id=sub_id, sub_name=sub_name, sem=sem, branch=branch)
        db.session.add(subject)
        db.session.commit()

    branches = Branchs.query.order_by(Branchs.branch_name).all()
    sub = Subjects.query.order_by(Subjects.sub_name).all()
    return render_template('admin/subject.html',branches=branches, sub=sub)



@app.route('/admin_attendance', methods=['GET', 'POST'])
@login_required
def admin_attendance():
    if request.method == 'POST':
        date = request.form['dates']
        branch = request.form['branch']
        sem = request.form['sem']
        sec = request.form['sec']
        sub = request.form['subs']
        
        if branch :
            quer = Students.query.filter(and_(Students.branch == branch, Students.sem == sem, Students.sec == sec)).all()
            return redirect(url_for('attendances', date=date, sub=sub, sem=sem, sec=sec, branch=branch))

    branches = Branchs.query.order_by(Branchs.branch_name).all()
    return render_template('admin/attendance.html', branches=branches)


@app.route('/attendances', methods=['GET', 'POST'])
@login_required
def attendances():
    sem = request.args.get('sem')
    sec = request.args.get('sec')
    branch = request.args.get('branch')
    quer = Students.query.filter(and_(Students.branch == branch, Students.sem == sem, Students.sec == sec)).all()
   
    if request.method == 'POST':
        date = request.form['dates']
        sub = request.form['sub']
        usn = request.form['usn']
        attend = request.form['atten']

        atten = Attendances(date=date, attendance=attend, subject=sub, usn=usn)
        db.session.add(atten)
        db.session.commit()
        
    return render_template('admin/attend_form.html', quer=quer, date=request.args.get('date'), sub = request.args.get('sub'))


@app.route('/attendance/<branch>,<sem>')
def sub(branch,sem):
    sems = Subjects.query.filter(
        and_(Subjects.branch == branch, Subjects.sem == sem))
     
    semArray = []

    for sem in sems:
        semObj ={}
        semObj['sub_id'] = sem.sub_id
        semObj['sub_name'] = sem.sub_id
        semArray.append(semObj)
    
    return jsonify({'sems':semArray})


@app.route('/timetable', methods=['GET', 'POST'])
@login_required
def timetable():
    form = TimeTable()

    if form.validate_on_submit():
        tb = TimeTables(val1=form.val1.data, val2=form.val2.data, val3=form.val3.data, val4=form.val4.data, val5=form.val5.data, val6=form.val6.data, val7=form.val7.data, val8=form.val8.data, val9=form.val9.data, val10=form.val10.data, val11=form.val11.data, val12=form.val12.data,val13=form.val13.data, val14=form.val14.data, val15=form.val15.data, val16=form.val16.data, val17=form.val17.data, val18=form.val18.data,val19=form.val19.data, val20=form.val20.data, val21=form.val21.data, val22=form.val22.data, val23=form.val23.data, val24=form.val24.data, val25=form.val25.data, val26=form.val26.data, val27=form.val27.data, val28=form.val28.data, val29=form.val29.data, val30=form.val30.data, val31=form.val31.data, val32=form.val32.data, val33=form.val33.data, val34=form.val34.data, val35 = form.val35.data, branch = form.branch.data, sem = form.sem.data, sec = form.sec.data)

        db.session.add(tb)
        db.session.commit()
    
    
    return render_template('admin/timetable.html',form=form )


##############################################################################################################
########################################  END ADMIN SECTION ##################################################
##############################################################################################################


##############################################################################################################
########################################  STUDENT  SECTION ##################################################
##############################################################################################################

@app.route('/student_dashboard')
@login_required
def student_dashboard():
     return render_template('student/dashboard.html')



@app.route("/account", methods=['GET', 'POST'])
@login_required
def student_account():
    form = StudentAccount()
    username = current_user.username

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,username)
            current_user.profile_image = picture_file

        current_user.s_user.first_name = form.fname.data
        current_user.s_user.last_name = form.lname.data
        current_user.s_user.address = form.address.data
        current_user.s_user.branch = form.branch.data
        current_user.s_user.sem = form.sem.data
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash("update Successfully")
        return redirect(url_for('student_account'))

    
    elif request.method == 'GET':
        form.usn.data = current_user.s_user.usn
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fname.data = current_user.s_user.first_name
        form.lname.data = current_user.s_user.last_name
        form.address.data = current_user.s_user.address
        form.branch.data = current_user.s_user.branch
        form.sem.data = current_user.s_user.sem

    image_file = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('student/user1.html', image_file=image_file, form=form)
   
@app.route('/student_info', methods=['GET', 'POST'])
@login_required
def student_info():
    if request.method == 'POST':
        usn = request.form['usn']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        branch = request.form['branch']
        sem = request.form['sem']
        sec = request.form['sec']

      
        
        if  Students.query.filter_by(usn=usn).first():
            flash("already submitted")
            return render_template('student/tables.html')

        else:
            student = Students(usn=usn, first_name=firstname, last_name=lastname,user_id=current_user.id, address=address, branch=branch,sem=sem,sec=sec)
            db.session.add(student)
            db.session.commit()
            flash("Information Add Successfully")
            return redirect(url_for('student_dashboard'))
    branches = Branchs.query.order_by(Branchs.branch_name).all()
    return render_template('student/tables.html',branches=branches)
        
@app.route('/assignment')
@login_required
def assignment():
     return render_template('student/assignment.html')
    
    


@app.route('/<username>')
def user_dashboard(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('student/dashboard.html', user=user)

##################################################################################################
##################################### student page End ###########################################
##################################################################################################

##################################################################################################
##################################### teacher coding area ########################################
##################################################################################################


@app.route('/teacher_dashboard', methods=['GET', 'POST'])
@login_required
def teacher_dashboard():

    form1 = AtimeTable()

    if form1.submit1.data and form1.validate_on_submit():
        branch = form1.branch.data
        sem = form1.sem.data
        sec = form1.sec.data
        return redirect(url_for('teacher_timetable',branch=branch,sem=sem,sec=sec))

    ############################## TEACHER BLOG ##############################
    if request.method == 'POST':
        if 'blog_submit' in request.form:
            title = request.form['title']
            topic = request.form['category']
            text = request.form['bolgdata']

            post = BlogPost(title=title, topic=topic,text=text, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
    ########################### End Teacher Blog ############################

    ############################## classroom ################################
    if request.method == 'POST':
        if 'sec' in request.form:
            branch = request.form['branch']
            sem = request.form['sem']
            sec = request.form['sec']
            return redirect(url_for('teacher_classroom', branch=branch, sem=sem, sec=sec))

    branches = Branchs.query.order_by(Branchs.branch_name).all()
    return render_template('teacher/dashboard.html', form1=form1,branches=branches)
    



    ####################


@app.route('/blogpost/<int:id>')
@login_required
def blogpost(id):
    data = BlogPost.query.get(id)

    return render_template('blog.html', data=data)




def save_picture(form_picture,username):
    
    filename = form_picture.filename
    ext_type = filename.split('.')[-1]
    picture_fn = str(username)+ '.' +ext_type
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
 
# Cropped image of above dimension
# (It will not change orginal image)


    output_size = (325, 325)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

####################### blog picture handiler#####################################
def blog_picture(form_picture, username):
    random_hex = secrets.token_hex(4)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/blog_pics', picture_fn)

# Cropped image of above dimension
# (It will not change orginal image)

    output_size = (325, 325)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/teacher_account", methods=['GET', 'POST'])
@login_required
def teacher_account():
    form = TeacherAccount()
    username = current_user.username

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,username)
            current_user.profile_image = picture_file

        current_user.t_user.first_name = form.fname.data
        current_user.t_user.last_name = form.lname.data
        current_user.t_user.address = form.address.data
        current_user.t_user.branch = form.branch.data
        current_user.username = form.username.data
        current_user.email = form.emailid.data
        
        db.session.commit()
        flash("update Successfully")
        return redirect(url_for('teacher_account'))

    elif request.method == 'GET':
        form.t_id.data = current_user.t_user.t_id
        form.username.data = current_user.username
        form.emailid.data = current_user.email
        form.fname.data = current_user.t_user.first_name
        form.lname.data = current_user.t_user.last_name
        form.address.data = current_user.t_user.address
        form.branch.data = current_user.t_user.branch
        
    image_file = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('teacher/user2.html', image_file=image_file, form=form)


@app.route('/teacher_info', methods=['GET', 'POST'])
@login_required
def teacher_info():
    if request.method == 'POST':
        t_id = request.form['t_id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        branch = request.form['branch']

        if Teachers.query.filter_by(t_id=t_id).first():
            flash("already submitted")
            return render_template('teacher/tables.html')

        else:
            teacher = Teachers(t_id = t_id, first_name = firstname,last_name=lastname, user_id=current_user.id, address=address,branch=branch)
            db.session.add(teacher)
            db.session.commit()
            flash("Information Add Successfully")
            return redirect(url_for('teacher_dashboard'))

    return render_template('teacher/tables.html')


@app.route('/teacher/timetable/<branch>/<sem>/<sec>', methods=['GET', 'POST'])
@login_required
def teacher_timetable(branch,sem,sec):
    form = TimeTable()

    quer = TimeTables.query.filter(and_(TimeTables.branch == branch, TimeTables.sem == sem, TimeTables.sec == sec)).first()
    
    if request.method == 'GET':
        form.val1.data = quer.val1
        form.val2.data = quer.val2
        form.val3.data = quer.val3
        form.val4.data = quer.val4
        form.val5.data = quer.val5
        form.val6.data = quer.val6
        form.val7.data = quer.val7
        form.val8.data = quer.val8
        form.val9.data = quer.val9
        form.val10.data = quer.val10
        form.val11.data = quer.val11
        form.val12.data = quer.val12
        form.val13.data = quer.val13
        form.val14.data = quer.val14
        form.val15.data = quer.val15
        form.val16.data = quer.val16
        form.val17.data = quer.val17
        form.val18.data = quer.val18
        form.val19.data = quer.val19
        form.val20.data = quer.val20
        form.val21.data = quer.val21
        form.val22.data = quer.val22
        form.val23.data = quer.val23
        form.val24.data = quer.val24
        form.val25.data = quer.val25
        form.val26.data = quer.val26
        form.val27.data = quer.val27
        form.val28.data = quer.val28
        form.val29.data = quer.val29
        form.val30.data = quer.val30
        form.val31.data = quer.val31
        form.val32.data = quer.val32
        form.val33.data = quer.val33
        form.val34.data = quer.val34

    
    return render_template('teacher/timetable.html',form=form,quer=quer)


@app.route('/teacher/classroom', methods=['GET', 'POST'])
def teacher_classroom():
    sem = request.args.get('sem')
    sec = request.args.get('sec')
    branch = request.args.get('branch')
    quer = Students.query.filter(and_(Students.branch == branch, Students.sem == sem, Students.sec == sec)).all()



    if 'notif_submit' in request.form and request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('teacher_classroom'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('teacher_classroom'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path,
                                   app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('teacher_classroom', filename=filename))
        else:
            flash("invalid file type")
            return redirect(url_for('teacher_classroom'))

    if 'atten_submit' in request.form and request.method == 'POST':
        date = request.form['dates']
        branch = request.form['branch']
        sem = request.form['sem']
        sec = request.form['sec']
        sub = request.form['subs']

        if branch:
            return redirect(url_for('attendances', date=date, sub=sub, sem=sem, sec=sec, branch=branch))

    branches = Branchs.query.order_by(Branchs.branch_name).all()
    return render_template('teacher/classroom.html',branches=branches)
#############################################################################################################



##############################################################################################################
########################################END TEACHER SECTION ##################################################
##############################################################################################################

@app.route('/compiler')
def compiler():
    return render_template('compiler.html')


@app.route('/blog', methods=['GET', 'POST'])
def blog():


    if request.method == 'POST':
        if 'blog_submit' in request.form:
            username = current_user.username
            picture_file = blog_picture(request.files['picture'], username)
            title = request.form['title']
            topic = request.form['category']
            text = request.form['bolgdata']

            post = BlogPost(title=title, topic=topic, text=text, blog_img = picture_file, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()

    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    blogmax = Blogcount.query.order_by(Blogcount.click.desc()).all()
    return render_template('blog/blog.html', blog_posts=blog_posts, blogmax=blogmax,count=request.args.get('count'))


@app.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    click = 0
    if blog_post_id:
        click = click+1
        blogid = Blogcount.query.filter_by(blog_id=blog_post_id).first()

        if blogid:
            blogid.click = blogid.click+1
            db.session.commit()
        else:
            blogclick = Blogcount(blog_id=blog_post_id, click=click)
            db.session.add(blogclick)
            db.session.commit()

    # grab the requested blog post by id number or return 404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog/blog-single.html', title=blog_post.title, date=blog_post.date, post=blog_post)


@app.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)


@app.route("/test",  methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',filename=filename))
        else:
            flash("invalid file type")
            return redirect(url_for('upload_file'))
    return render_template('admin/testing.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
