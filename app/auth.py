from functools import wraps

import jwt
from flask import request, jsonify, current_app

from app.models import User

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']

        if not token:
            return jsonify({ 'error': 'Voce nao pode acessar essa rota' }), 403

        if not 'Bearer' in token:
            return jsonify({ 'error': 'Token invalido' }), 401

        try:
            token_pure = token.replace('Bearer ', '')
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'])
            current_user = User.query.get(decoded['id'])
        except:
            return jsonify({
                'error': 'O token nao e valido'
            }), 401

        return f(current_user=current_user, *args, **kwargs)

    return wrapper