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
parser.add_argument('role', required=True, type=int)


class RolesResource(Resource):
    def get(self):
        args = parser.parse_args()
        session = db_session.create_session()
        role = session.get(Role, args['role'])
        main_key = session.get(Role, 8)
        if 1 <= role.id <= 7 and main_key.check_key(args['api_key']):
            key = ''.join(random.choices(ALPHABET, k=30))
            role.set_key(key)
            session.commit()
            return jsonify({'api_key': key,
                            'role_id': args['role']
                            })
        else:
            return jsonify({'error': 'Что-то пошло не так'})
