from flask import Flask, render_template, redirect, request, make_response
from flask import session, abort
from data import db_session, users_resource, resource_roles
from data.users import User
from data.news import News
from data.letter import Letter
from data.roles import Role
from forms.authorization import LoginForm, RegisterForm, SearchForm
from forms.feedback import LetterForm
from forms.users import ApiForm
from forms.news import NewsForm1, NewsForm2, NewsForm3
import os
import datetime as dt
from flask_restful import reqparse, abort, Api, Resource
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from waitress import serve

# Создаем приложение
app = Flask(__name__)
app.config['SECRET_KEY'] = '&&&&&&&&&&'
# Создаем Api для приложения.
api = Api(app)
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=1)
# Инициализируем LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


# Функция для получения пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Функция для выхода из аккаунта пользователя.
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Обработчик для добавления новости.
@app.route('/news/<int:id_news>', methods=['GET', 'POST'])
@login_required
def add_news(id_news):
    # Есть три типа новости:
    #     1) Текст
    #     2) Текст + Фото
    #     3) Текст + Видео
    # В зависимости какой тип новости мы обрабатываем форму и создаем новость.
    # Пользователям рангом меньше 4 запрещено взаимодействовать с этой функцией.
    if current_user.roles_id < 4:
        return redirect('/')
    if id_news == 1:
        form = NewsForm1()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = News()
            news.title = form.title.data
            news.content = form.content.data
            news.type = 1
            current_user.news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('news1.html', title='Добавление новости',
                               form=form)
    elif id_news == 2:
        form = NewsForm2()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = News()
            news.title = form.title.data
            news.content = form.content.data
            news.photo = form.photo.data
            news.type = 2
            current_user.news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('news2.html', title='Добавление новости',
                               form=form)
    elif id_news == 3:
        form = NewsForm3()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = News()
            news.title = form.title.data
            news.content = form.content.data
            video = form.video.data
            # Данная замена нужна, чтобы обойти блокировку источника видео.
            video = video.replace('youtu.be/', 'www.youtube.com/embed/')
            news.video = video
            news.type = 3
            current_user.news.append(news)
            db_sess.merge(current_user)
            db_sess.commit()
            return redirect('/')
        return render_template('news3.html', title='Добавление новости',
                               form=form)


# Обработчик для удаления новости
@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    # Пользователям рангом меньше 4 запрещено взаимодействовать с этой функцией.
    if current_user.roles_id < 4:
        return redirect('/')
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    # Если переданная ноость есть, мы ее удаляем.
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# Обработчик для редактирования новости.
@app.route('/news/<int:id_news>/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id_news, id):
    db_sess = db_session.create_session()
    # Проверяем на наличие новости.
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    # Пользователям рангом меньше 4 запрещено взаимодействовать с этой функцией.
    if current_user.roles_id < 4:
        return redirect('/')
    if not news:
        abort(404)
    id_news = news.type
    # Есть три типа новости:
    #     1) Текст
    #     2) Текст + Фото
    #     3) Текст + Видео
    # В зависимости какой тип новости мы обрабатываем форму и редактируем новость.
    if id_news == 1:
        form = NewsForm1()
        if request.method == "GET":
            form.title.data = news.title
            form.content.data = news.content
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = db_sess.query(News).filter(News.id == id,
                                              News.user == current_user
                                              ).first()
            if news:
                news.title = form.title.data
                news.content = form.content.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('news1.html',
                               title='Редактирование новости',
                               form=form
                               )
    elif id_news == 2:
        form = NewsForm2()
        form.title.data = news.title
        form.content.data = news.content
        form.photo.data = news.photo

        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = db_sess.query(News).filter(News.id == id,
                                              News.user == current_user
                                              ).first()
            if news:
                news.title = form.title.data
                news.content = form.content.data
                news.photo = form.photo.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('news2.html',
                               title='Редактирование новости',
                               form=form
                               )
    elif id_news == 3:
        form = NewsForm3()
        if request.method == "GET":
            form.title.data = news.title
            form.content.data = news.content
            form.video.data = news.video

        if form.validate_on_submit():
            db_sess = db_session.create_session()
            news = db_sess.query(News).filter(News.id == id,
                                              News.user == current_user
                                              ).first()
            if news:
                news.title = form.title.data
                news.content = form.content.data
                video = form.video.data
                video = video.replace('youtu.be/', 'www.youtube.com/embed/')
                news.video = video
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('news3.html',
                               title='Редактирование новости',
                               form=form
                               )


# Обработчик для прочитывания письма.
@app.route('/letter_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def letter_delete(id):
    db_sess = db_session.create_session()
    # Пользователям рангом меньше 4 запрещено взаимодействовать с этой функцией.
    if current_user.roles_id < 4:
        return redirect('/')
    for letter in current_user.letters:
        if letter.id == id:
            # Мы удаляем из почты пользователя письмо и сохраняем изменения в БД
            current_user.letters.remove(letter)
            db_sess.merge(current_user)
            db_sess.commit()
        else:
            # Скорее всего были переданы неверные данные.
            abort(404)
    return redirect('/profile')


# Обработчик главной страницы сайта
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    feedback_form = LetterForm()
    top_users = []
    top_img = []
    news = db_sess.query(News).all()
    # Получаем список всех участников ученического совета.
    for role in db_sess.query(Role).filter(Role.id >= 2, Role.id < 8).all():
        for i, user in enumerate(role.users):
            top_users.append(user)
            # Здесь мы получаем фотографию пользователя из БД
            IMG = f'static/img/user/avatar.png'
            top_img.append(IMG)
    # Обрабатываем форму обратной связи.
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
            return redirect('/')
    return render_template("index.html", feedback_form=feedback_form,
                           top_list=top_img, top_users=top_users, news=news,
                           title='ГЛАВНАЯ СТРАНИЦА САЙТА')


# Обработчик авторизации.
@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            # Если все хорошо, авторизуемся
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('authorization.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('authorization.html', title='Авторизация', form=form)


# Обработчик регистрации
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
        # Заполняем всю информацию о пользователе и сохраняем в БД
        user.nickname = form.nickname.data
        user.set_password(form.password.data)
        user.surname = form.surname.data
        user.name = form.name.data
        user.patronymic = form.patronymic.data
        user.about = form.about.data
        user.avatar = f'static/img/user/avatar.png'
        db_sess.add(user)
        db_sess.commit()
        return redirect("/authorization")
    return render_template('registration.html', title='Регистрация', form=form)


# Обработчика профиля пользователя
@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    session = db_session.create_session()
    message = ''
    api_form = ApiForm()
    # Вводим api-key и если все хорошо, то даем пользователю новую роль.
    if api_form.data['submit']:
        roles = session.query(Role).all()
        key = api_form.data['apikey']
        # Проверяем на совпадение ключа роли с ключом, который был введен.
        for role in roles:
            if role.check_key(key) and role.is_activity:
                if current_user.roles_id > role.id:
                    message = 'Ваша роль лучше чем та, которую вы пытаетесь активировать'
                    break
                current_user.roles_id = role.id
                role.is_activity = 0
    session.merge(current_user)
    session.commit()
    role = session.query(Role).get(current_user.roles_id)
    # Получаем всю почту пользователя
    letters = current_user.letters
    IMG = f'static/img/user/avatar.png'
    f = current_user.avatar
    surname = current_user.surname
    name = current_user.name
    patronymic = current_user.patronymic
    about = current_user.about
    param = {'api_form': api_form,
             'status': role.name,
             'letters': letters,
             'avatar': IMG,
             'surname': surname,
             'name': name,
             'patronymic': patronymic,
             'about': about,
             'message': message
             }
    return render_template('user.html', **param)


def main():
    db_session.global_init('db/datebase.db')
    port = int(os.environ.get("PORT", 5000))
    # Добавляем в api все созданные нами ресурсы
    api.add_resource(users_resource.UsersListResource, '/api/users')
    api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(resource_roles.RoleListResource, '/api/roles')
    api.add_resource(resource_roles.RoleResource, '/api/roles/<int:role_id>')
    api.add_resource(resource_roles.KeyResource, '/api/key_roles/<int:role_id>')
    session = db_session.create_session()
    user = session.query(User).get(1)
    user.set_password('mWa90jB90cn3ReE')
    user = session.query(User).get(2)
    user.set_password('OivnkvEOr7EygEF')
    user = session.query(User).get(3)
    user.set_password('eKhkBN8iAsEUpjE')
    user = session.query(User).get(4)
    user.set_password('AF3s9l0BInhRWSK')
    user = session.query(User).get(5)
    user.set_password('0mJtnQgOJ02CQ5n')
    user = session.query(User).get(6)
    user.set_password('caSw5pW7YiX95fH')
    user = session.query(User).get(7)
    user.set_password('IDrKFHYtHZW6dsK')
    user = session.query(User).get(8)
    user.set_password('Q9NyaqEdHQExShT')
    user = session.query(User).get(9)
    user.set_password('UdZuHHErHMweOoB')
    user = session.query(User).get(10)
    user.set_password('SpttBd3FurtQAxN')
    user = session.query(User).get(11)
    user.set_password('aRVDSWaLkqe0Dik')
    user = session.query(User).get(12)
    user.set_password('iIU34RhKLGnw4cf')
    user = session.query(User).get(13)
    user.set_password('a3q8zcKUAqUezax')
    user = session.query(User).get(14)
    user.set_password('FgstXUlgdxG2brz')
    user = session.query(User).get(15)
    user.set_password('1234567890aA')
    role = session.query(Role).get(1)
    role.set_key('Wr96llTyl4NTZXiojDV8jGQZpIz9QI')
    role = session.query(Role).get(2)
    role.set_key('2SxICRKpj3cFFj31lrH8MZaiw0mbLO')
    role = session.query(Role).get(3)
    role.set_key('vs0PulLpA8M4ilNFrR8MSF8ApihXya')
    role = session.query(Role).get(4)
    role.set_key('kBxPeAL3zDchLBowg9r421ZqSNaWFc')
    role = session.query(Role).get(5)
    role.set_key('vLIOr8PLAVn5wWe9eBep99WeVND3DB')
    role = session.query(Role).get(6)
    role.set_key('nu6dcP0bFbmG0CN4xdJIaOK7akwQPk')
    role = session.query(Role).get(7)
    role.set_key('eJfveJ0JA7mUee1xiX5fHzCBJd9q8c')
    role = session.query(Role).get(8)
    role.set_key('extymtbnhelltytuvytlflen')
    serve(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
