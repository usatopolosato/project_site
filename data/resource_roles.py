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


class KeyResource(Resource):
    def get(self, role_id):
        args = parser.parse_args()
        session = db_session.create_session()
        role = session.get(Role, role_id)
        if not role:
            abort(404, message=f'Role {role_id} not found')
        main_key = session.get(Role, 8)
        if 2 <= role.id <= 7 and main_key.check_key(args['api_key']):
            key = ''.join(random.choices(ALPHABET, k=30))
            role.set_key(key)
            session.commit()
            return jsonify({'api_key': key,
                            'role_id': role_id
                            })
        else:
            return jsonify({'error': 'Что-то пошло не так'})


class RoleListResource(Resource):
    def get(self):
        session = db_session.create_session()
        roles = session.query(Role).all()
        return jsonify({'roles': [item.to_dict(
            only=('name', 'description')) for item in roles]})


class RoleResource(Resource):
    def get(self, role_id):
        session = db_session.create_session()
        role = session.get(Role, role_id)
        if not role:
            abort(404, message=f'Role {role_id} not found')
        return jsonify({'roles': role.to_dict(
            only=('name', 'description'))})
