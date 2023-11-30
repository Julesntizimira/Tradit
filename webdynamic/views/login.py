from webdynamic.views import app_pages
from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, IntegerField
from wtforms.validators import input_required, Length, ValidationError, Email
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf.file import FileField, FileAllowed
from flask_bcrypt import Bcrypt
from models import storage
from models.user import User

bcrypt = Bcrypt()

class LoginForm(FlaskForm):
    '''Login form'''
    username = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")
    remember = BooleanField("Remember Me")


class RegisterForm(FlaskForm):
    '''Registration Form'''
    name = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Name"})
    address = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Address"})
    username = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    email = EmailField(validators=[input_required(), Email(message="Invalid email address")], render_kw={"placeholder":"Email"})
    password = PasswordField(validators=[input_required(), Length(min=4, max=20), ], render_kw={"placeholder":"Password"})
    file = FileField('file', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = storage.session.query(User).filter(User.username == username.data).first()
        if existing_user_username:
            raise ValidationError("that username already exists please choose a different one" )


@app_pages.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app_pages.route('/register', methods=['GET', 'POST'])
def register():
    from webdynamic.handleImage import handleImage
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        file = form.file.data
        handleImage(file, form.name.data, 'profiles')
        new_user = User(username=form.username.data, password=hashed_password,  name=form.name.data, email=form.email.data, address=form.address.data)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)