# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from myproject.models import User , Subjects


class StudForm(FlaskForm):
    usn = StringField('Usn', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    emailid = StringField('Email Address', validators=[
                          DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), EqualTo('confpwd', message='Passwords must match')])
    confpwd = PasswordField('Confirm Password', validators=[DataRequired()])
    usertype = StringField('User Type', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    submit = SubmitField('Submit')


class TechForm(FlaskForm):
    tech_id = StringField('Teacher Id', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    emailid = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), EqualTo('confpwd', message='Passwords must match')])
    confpwd = PasswordField('Confirm Password', validators=[DataRequired()])
    usertype = StringField('User Type', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')


class BranchForm(FlaskForm):
    sems = [('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),('9', '9'),('10', '10')]
    branch_id = StringField('Branch Code', validators=[DataRequired()])
    branch_name = StringField('Branch Name', validators=[DataRequired()])
    sem = SelectField('Semester', choices=sems)
    submit = SubmitField('Submit')








class TeacherAccount(FlaskForm):
    t_id = StringField('Teacher Id', validators=[])
    username = StringField('Username', validators=[DataRequired()])
    emailid = StringField('Email Address', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class StudentAccount(FlaskForm):
    sems = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')]
    usn = StringField('Teacher Id', validators=[])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    sem = SelectField('Semester', choices=sems)
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')



class TimeTable(FlaskForm):
    sems = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')]
    secs = [('A','A'), ('B', 'B'), ('C', 'C')]
    val1 = StringField('sub1', validators=[DataRequired()])
    val2 = StringField('sub1', validators=[DataRequired()])
    val3 = StringField('sub1', validators=[DataRequired()])
    val4 = StringField('sub1', validators=[DataRequired()])
    val5 = StringField('sub1', validators=[DataRequired()])
    val6 = StringField('sub1', validators=[DataRequired()])
    val7 = StringField('sub1', validators=[DataRequired()])
    val8 = StringField('sub1', validators=[DataRequired()])
    val9 = StringField('sub1', validators=[DataRequired()])
    val10 = StringField('sub1', validators=[DataRequired()])
    val11 = StringField('sub1', validators=[DataRequired()])
    val12 = StringField('sub1', validators=[DataRequired()])
    val13 = StringField('sub1', validators=[DataRequired()])
    val14 = StringField('sub1', validators=[DataRequired()])
    val15 = StringField('sub1', validators=[DataRequired()])
    val16 = StringField('sub1', validators=[DataRequired()])
    val17 = StringField('sub1', validators=[DataRequired()])
    val18 = StringField('sub1', validators=[DataRequired()])
    val19 = StringField('sub1', validators=[DataRequired()])
    val20 = StringField('sub1', validators=[DataRequired()])
    val21 = StringField('sub1', validators=[DataRequired()])
    val22 = StringField('sub1', validators=[DataRequired()])
    val23 = StringField('sub1', validators=[DataRequired()])
    val24 = StringField('sub1', validators=[DataRequired()])
    val25 = StringField('sub1', validators=[DataRequired()])
    val26 = StringField('sub1', validators=[DataRequired()])
    val27 = StringField('sub1', validators=[DataRequired()])
    val28 = StringField('sub1', validators=[DataRequired()])
    val29 = StringField('sub1', validators=[DataRequired()])
    val30 = StringField('sub1', validators=[DataRequired()])
    val31 = StringField('sub1', validators=[DataRequired()])
    val32 = StringField('sub1', validators=[DataRequired()])
    val33 = StringField('sub1', validators=[DataRequired()])
    val34 = StringField('sub1', validators=[DataRequired()])
    val35 = StringField('sub1', validators=[DataRequired()])
    branch = StringField('Branch', validators=[DataRequired()])
    sem = SelectField('Semester', choices=sems)
    sec = SelectField('Sec', choices=secs)
    submit = SubmitField('Submit')

    
class AtimeTable(FlaskForm):
    sems = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
            ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')]
    secs = [('A','A'), ('B', 'B'), ('C', 'C')]
    branch = StringField('Branch', validators=[DataRequired()])
    sem = SelectField('Semester', choices=sems)
    sec = SelectField('Sec', choices=secs)
    submit1 = SubmitField('Submit')
