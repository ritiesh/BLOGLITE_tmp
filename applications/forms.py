# import form as form
from flask_login import LoginManager
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
# from flask_uploads import UploadSet, IMAGES, configure_uploads
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, SelectField, form, TextAreaField
from wtforms.validators import InputRequired, ValidationError, Length
from applications.models import *


class signupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={'style':'padding:5px;border:1px solid #ccc;border-radius:3px',"placeholder": "Username"})
    f_name = StringField('First Name', validators=[InputRequired()],render_kw={'style':'padding:5px;border:1px solid #ccc;border-radius:3px',"placeholder": "Firstname"})
    l_name = StringField('Last Name', validators=[InputRequired()],render_kw={'style':'padding:5px;border:1px solid #ccc;border-radius:3px',"placeholder": "Lastname"})
    email = StringField('Email', validators=[InputRequired()], render_kw={'style':'padding:5px;border:1px solid #ccc;border-radius:3px',"placeholder": "Email"})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={'style':'padding:5px;border:1px solid #ccc;border-radius:3px',"placeholder": "Password"})
    submit = SubmitField('Signup',render_kw={'style':'width:70px;background-color:blue;color:white;margin-left:90px;border:none;border-radius:3px;padding:5px'})

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError('Username already exists')


class signinForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={'style':'width:30ch',"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=100)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField('Login',render_kw={'style':'width:70px;background-color:blue;color:white;margin-left:100px'})


class PostForm(FlaskForm):
    desc = StringField('Text')
    img = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'])])  # IMAGE
    post = SubmitField('Post')


class Searchform(FlaskForm):
    search = StringField('Username', validators=[InputRequired()])
    # submit = SubmitField('Search')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    # img = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    about_me = TextAreaField('About_me', validators=[Length(min=0, max=100)])
    submit = SubmitField('Update')


class EditPostForm(FlaskForm):
    desc = StringField('Description')
    img = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'])])  # IMAGE
    update = SubmitField('Update')
