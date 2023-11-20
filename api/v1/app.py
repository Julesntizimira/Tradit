from flask import Flask, render_template, make_response, jsonify, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import input_required, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from models.user import User
from models import storage


from api.v1.views import app_views

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SESSION_PROTECTION'] = 'strong'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)
    return storage.session.query(User).get(user_id)


class RegisterForm(FlaskForm):
    name = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Name"})
    address = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Address"})
    username = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    email = EmailField(validators=[input_required(), Email(message="Invalid email address")], render_kw={"placeholder":"Email"})
    password = PasswordField(validators=[input_required(), Length(min=4, max=20), ], render_kw={"placeholder":"Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = storage.session.query(User).filter(User.username == username.data).first()
        if existing_user_username:
            raise ValidationError("that username already exists please choose a different one" )

class LoginForm(FlaskForm):
    username = StringField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[input_required(), Length(min=4, max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")
    remember = BooleanField("Remember Me")


app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

@app.route('/')
def home():
    return render_template('landing1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5200', debug=True)
