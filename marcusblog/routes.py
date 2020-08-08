from flask import render_template, url_for, flash, redirect
from marcusblog import app, db, bcrypt
from marcusblog.forms import RegistrationForm, LoginForm
from marcusblog.models import User,Post
from flask_login import login_user

posts = [
    {
        'author': 'BATMAN',
        'title': 'Arkham C  ity',
        'content': 'First post',
        'date_posted': 'jun 20, 2020'
    },
    {
        'author': 'BRUCE WAYNE',
        'title': 'Arkham Asylum',
        'content': 'Second post',
        'date_posted': 'jun 21, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit() 
        flash(f"hey! {form.username.data} Your account has been created, Please user your email ID and password to login!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember-form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email ID and password', 'danger')
    return render_template('login.html', title='Login', form=form)