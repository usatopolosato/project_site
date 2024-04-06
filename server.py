from flask import Flask, render_template, redirect, request, make_response
from flask import session, abort
from data import db_session
from data.users import User
from data.letter import Letter
from data.roles import Role
from forms.authorization import LoginForm, RegisterForm
from forms.feedback import LetterForm
import os
import datetime as dt
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '&&&&&&&&&&'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=1)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    feedback_form = LetterForm()
    if feedback_form.validate_on_submit():
        if current_user.is_authenticated:
            choice = {0: 'Предложение', 1: 'Жалоба'}
            if len(feedback_form.content.data) < 5 or len(feedback_form.content.data.split()) < 2:
                return render_template("index.html", feedback_form=feedback_form,
                                       message='Ошибка обработки сообщения')
            db_sess = db_session.create_session()
            letter = Letter(title=choice[feedback_form.data['title']],
                            content=feedback_form.content.data)
            for role in db_sess.query(Role).filter(Role.id >= 3).all():
                for user in role.users:
                    user.letters.append(letter)
            db_sess.commit()
    return render_template("index.html", feedback_form=feedback_form)


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('authorization.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('authorization.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.data['submit']:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        if user:
            return render_template('registration.html',
                                   message="Пользователь с таким логином уже существует...",
                                   form=form)
        user = User()
        user.nickname = form.nickname.data
        user.set_password(form.password.data)
        user.surname = form.surname.data
        user.name = form.name.data
        user.patronymic = form.patronymic.data
        user.about = form.about.data
        # user.avatar = form.avatar.data
        print(user.avatar)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/authorization")
    return render_template('registration.html', title='Регистрация', form=form)


def main():
    db_session.global_init('db/datebase.db')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
