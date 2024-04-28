from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import RegisterForm, LoginForm
from data.users import User
from data import db_session
import random
import sqlite3
from flask import Flask, url_for, request, render_template, redirect, request, abort
from flask import send_file
# from admin_files import new_task_to_db
# from new_task_to_db import new_task_to_db
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


@app.route('/adminpage', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    print('Какая-то страница № 1')
    return redirect('/')


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

        # без базы данных
        # al = ['/static/img/1280.gif', '/static/img/1267.gif', '/static/img/1276.gif', '/static/img/1270.gif']
        # img = random.choice(al)
        # del al[al.index(img)]
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
    if request.method == 'GET':
        return render_template('admin_page.html')
    elif request.method == 'POST':
        # print(request.form.get("file_photo", ""))
        # print(request.form.get("num", ""))
        new_task(request.form.get("file_photo", ""), request.form.get("num", ""))
        return render_template('admin_page.html')


def res_json():
    print(my_user.clas)
    print(my_user.name)
    for i in range(3):
        my_user.result.append([my_user.res_task[i], my_user.res_des[i]])
    print(my_user.result)


def tasks(my_counter, img):
    my_counter.counter += 1
    return render_template('tasks_page.html', img=img)


def new_task(photo_name, num):
    if int(num) in [1, 2, 3]:
        print(photo_name, num)


if __name__ == '__main__':
    main()
