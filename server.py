import io

from PIL import Image
from flask import Flask, render_template, redirect, request, make_response
from flask import session, abort
from data import db_session, users_resource, resource_roles
from data.users import User
from data.letter import Letter
from data.roles import Role
from forms.authorization import LoginForm, RegisterForm
from forms.feedback import LetterForm
from forms.users import UserForm, ApiForm
import os
import datetime as dt
from flask_restful import reqparse, abort, Api, Resource
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = '&&&&&&&&&&'
api = Api(app)
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
    db_sess = db_session.create_session()
    feedback_form = LetterForm()
    top_users = []
    top_img = []
    for role in db_sess.query(Role).filter(Role.id >= 1, Role.id < 8).all():
        for i, user in enumerate(role.users):
            top_users.append(user)
            IMG = f'static/img/top/{i}-top.png'
            f = user.avatar
            # rawIO = io.BytesIO(f)
            # rawIO.seek(0)
            # byteImg = Image.open(rawIO)
            # byteImg.save('test.png', 'PNG')
            try:
                with open(IMG, "wb+") as file:
                    file.write(f)
                img = Image.open(f'static/img/top/{i}-top.png')
                w = img.size[0]
                h = img.size[1]
                image = img.crop(((w - h) // 2, 0, w // 2 + h // 2, h))
                image.save(f'static/img/top/{i}-top.png')
                top_img.append(IMG)
            except Exception:
                continue
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
    return render_template("index.html", feedback_form=feedback_form,
                           top_list=top_img, top_users=top_users)


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
        avatar = request.files['avatar']
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
        user.avatar = avatar.read()
        db_sess.add(user)
        db_sess.commit()
        return redirect("/authorization")
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    session = db_session.create_session()
    exit_form = UserForm()
    api_form = ApiForm()
    if exit_form.data['submit']:
        return redirect("/logout")
    if api_form.data['submit']:
        roles = session.query(Role).all()
        key = api_form.data['apikey']
        for role in roles:
            if role.check_key(key) and role.is_activity:
                if current_user.roles_id > role.id:
                    param = {'api_form': api_form,
                             'exit_form': exit_form,
                             'message': 'Ваша роль лучше чем та, которую вы пытаетесь активировать'}
                    return render_template('user.html', **param)
                current_user.roles_id = role.id
                role.is_activity = 0
                session.commit()
                break
    role = session.get(Role, current_user.roles_id)
    letters = current_user.letters
    IMG = f'static/img/user/avatar.png'
    f = current_user.avatar
    print(f)
    with open(IMG, "wb+") as file:
        file.write(f)
    param = {'api_form': api_form,
             'exit_form': exit_form,
             'status': 'role.name',
             'letters': letters,
             'avatar': IMG
             }
    return render_template('user.html', **param)


def main():
    db_session.global_init('db/datebase.db')
    port = int(os.environ.get("PORT", 5000))
    api.add_resource(users_resource.UsersListResource, '/api/users')
    api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(resource_roles.RoleListResource, '/api/roles')
    api.add_resource(resource_roles.RoleResource, '/api/roles/<int:role_id>')
    api.add_resource(resource_roles.KeyResource, '/api/key_roles/<int:role_id>')
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
