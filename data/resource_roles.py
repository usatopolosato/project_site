from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from . import db_session
import random
from .roles import Role
from string import ascii_letters

ALPHABET = ascii_letters + '1234567890'

parser = reqparse.RequestParser()
parser.add_argument('api_key', required=True)


# Данный ресурс предназначен для генерации ключей, нужных для получения новой роли.
class KeyResource(Resource):
    def get(self, role_id):
        try:
            args = parser.parse_args()
            session = db_session.create_session()
            role = session.get(Role, role_id)
            if not role:
                abort(404, message=f'Role {role_id} not found')
            main_key = session.query(Role).get(8)
            # Мы передаем api-ключ разработчика для доступа к генерации новых api-keys.
            if 2 <= role.id <= 7 and main_key.check_key(args['api_key']):
                # Если ключ введен верно, то мы генерируем новый ключ для данной роли.
                key = ''.join(random.choices(ALPHABET, k=30))
                role.set_key(key)
                role.is_activity = 1
                session.commit()
                return jsonify({'api_key': key,
                                'role_id': role_id
                                })
            else:
                return jsonify({'error': 'Что-то с БД'})
        except Exception:
            return jsonify({'error': 'Что-то пошло не так'})


# Ресурс предназначен для получения информации о всех ролях(В доработках мы сможем узнать описание
# всех возможностей данных привилегий)
class RoleListResource(Resource):
    def get(self):
        try:
            session = db_session.create_session()
            roles = session.query(Role).all()
            return jsonify({'roles': [item.to_dict(
                only=('name', 'description')) for item in roles]})
        except Exception:
            return jsonify({'error': 'Что-то пошло не так'})


# Ресурс предназначен для получения информации о конкретной роли(В доработках мы сможем узнать
# описание всех возможностей данной привилегии)
class RoleResource(Resource):
    def get(self, role_id):
        try:
            session = db_session.create_session()
            role = session.query(Role).get(role_id)
            if not role:
                abort(404, message=f'Role {role_id} not found')
            return jsonify({'roles': role.to_dict(
                only=('name', 'description'))})
        except Exception:
            return jsonify({'error': 'Что-то пошло не так'})
