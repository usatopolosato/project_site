import sqlalchemy
import datetime
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


# Таблица для хранения содержимого письма(feedback).
class Letter(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'letters'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)


# У пользователя в почтовом ящике может быть несколько писем, для того создадим
# ассоциативную таблицу.
association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('letters', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('letters.id'))
)
