import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


# Таблица для хранения информации о привилегиях.
class Role(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    # Храним ключ секретно, чтобы злоумышленники не смогли воспользоваться всеми функциями сайта.
    secret_key = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    color = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_activity = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    users = orm.relationship("User", back_populates='roles')

    # Метод для установки секретного api-ключа.
    def set_key(self, key):
        self.secret_key = generate_password_hash(key)

    # Метод, который проверяет правильность введенного пользователем api-ключа.
    def check_key(self, key):
        return check_password_hash(self.secret_key, key)
