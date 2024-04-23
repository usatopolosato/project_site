import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


# Таблица для хранения информации о пользователе.
class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    # Пароль хэшируем, чтобы злоумышленники не смогли его узнать и взломать пользователя.
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # Связь с таблицами News и Roles.
    news = orm.relationship("News", back_populates='user')
    letters = orm.relationship("Letter",
                               secondary="association",
                               backref="users")
    roles_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id"), default=1)
    avatar = sqlalchemy.Column(sqlalchemy.BINARY, nullable=True)

    roles = orm.relationship('Role')

    # Метод для установки нового пароля пользователя.
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # Метод для проверки правильности введеного пользователем пароля.
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
