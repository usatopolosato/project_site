from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from werkzeug.security import generate_password_hash
from . import db_session
from .users import User
from .roles import Role

parser = reqparse.RequestParser()
parser.add_argument('api_key', required=True)


# Ресурс для работы с пользователем.
class UsersResource(Resource):
    # Метод для получения информации о конкретном пользователе.
    def get(self, user_id):
        try:
            session = db_session.create_session()
            user = session.query(User).get(user_id)
            if not user:
                abort(404, message=f'User {user_id} not found')
            return jsonify({'user': user.to_dict(
                only=('surname', 'name', 'about', 'id'))})
        except Exception:
            return jsonify({'error': 'Что-то пошло не так'})

    # Метод предназначен для удаления пользователя
    # по ключу разработчика(пользоваться нужно с осторожностью)
    def delete(self, user_id):
        try:
            session = db_session.create_session()
            main_key = session.query(Role).get(8)
            args = parser.parse_args()
            if main_key.check_key(args['api_key']):
                user = session.query(User).get(user_id)
                if not user:
                    abort(404, message=f'User {user_id} not found')
                session.delete(user)
                session.commit()
                return jsonify({'success': 'OK'})
            return jsonify({'error': 'Что-то пошло не так'})
        except Exception:
            return jsonify({'error': 'Что-то пошло не так'})


# Ресурс для получения информации о всех пользователях.
class UsersListResource(Resource):
    def get(self):
        try:
            session = db_session.create_session()
            roles = session.query(Role).filter(Role.id >= 1, Role.id < 8).all()
            users = []
            for role in roles:
                users += role.users
            return jsonify({'users': [item.to_dict(
                only=('surname', 'name', 'patronymic', 'about', 'id')) for item in users]})
        except Exception:
            return jsonify({'error': 'Что-то пошло не так'})
