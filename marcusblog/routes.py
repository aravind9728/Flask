import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from marcusblog import app, db, bcrypt
from marcusblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from marcusblog.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Incorrect username or password. Please enter your correct username and password or click forget password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(from_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(from_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    from_picture.save(picture_path)

    output_size = (125, 125)
    rs = Image.open(from_picture)
    rs.thumbnail(output_size)
    rs.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form=form)

    @app.route("/post/new", methods=['GET', 'POST')
    @login_required
    def new_post():
        form = 'PostForm'
        if form.validate_on_submit():
            flash(f'Your post has been created!', 'success')
            return redirect(url_for('home'))
        return render_template('create_post.html', title = 'New Post')



