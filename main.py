from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm, LoginForm
from data.users import User
from data import db_session
import random
import sqlite3
from flask import render_template
from flask import send_file
from json_file import res_file
import os
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.secret_key = "secret key"
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User_start():
    def __init__(self):
        self.clas = ''
        self.name = ''
        self.res_task = []
        self.res_des = []
        self.result = []


class Decision():
    def __init__(self):
        self.result = []


class Counter():
    def __init__(self):
        self.counter = 1


my_counter = Counter()
my_results = Decision()
my_user = User_start()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/', methods=['POST', 'GET'])
def start_page():
    if request.method == 'GET':
        return render_template('home_page.html')
    elif request.method == 'POST':

        DB = sqlite3.connect('DB/test_web.db')
        SQL = DB.cursor()
        al = SQL.execute(f"SELECT * FROM task WHERE number == {my_counter.counter}").fetchall()
        img = ''
        if my_counter.counter <= 3:
            list_img = [i[1] for i in al]
            img = str(random.choice(list_img))

        name = request.form
        if 'name' in name:
            my_user.clas = str(name.getlist('clas'))
            my_user.name = f"{str(name.getlist('name')[0])}"
            my_user.res_task.append(img)

        elif 'decision' in name:
            if img != '':
                my_user.res_task.append(img)
            my_user.res_des.append(str(name.getlist('decision')[0]))
        if my_counter.counter == 4:
            res_json()
            return render_template('end_page.html')
        return tasks(my_counter, img)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/admin_page', methods=['POST', 'GET'])
def admin_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_task(filename, request.form.getlist('num')[0])
            render_template('admin_page.html')
    return render_template('admin_page.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/download_json', methods=['POST', 'GET'])
def download_json():
    return send_file('result.json')


def res_json():
    for i in range(3):
        my_user.result.append([my_user.res_task[i], my_user.res_des[i]])
    res_file(my_user.name, my_user.clas, my_user.result)


def tasks(my_counter, img):
    my_counter.counter += 1
    return render_template('tasks_page.html', img=img)


def new_task(photo_name, num):
    DB = sqlite3.connect('DB/test_web.db')
    SQL = DB.cursor()
    a = int(num)
    b = '/static/img/' + photo_name
    SQL.execute(f"INSERT INTO Task Values (?, ?)", (a, b))
    DB.commit()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    main()
