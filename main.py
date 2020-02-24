from flask import jsonify, request
from flask_migrate import Migrate

import datetime
import jwt

from app import app, db, dbPath
from app.models import User, user_share_schema, users_share_schema
from app.auth import jwt_required

Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        dbPath=dbPath
    )

@app.cli.command()
def createdb():
    """Create DB"""
    db.create_all()


@app.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

        user = User(
            username,
            email,
            password
        )

        db.session.add(user)
        db.session.commit()

        result = user_share_schema.dump(
            User.query.filter_by(email=email).first()
        )

        return jsonify(result)


@app.route('/auth/login', methods=['POST'])
def login():
    password = request.json['password']
    email = request.json['email']

    user = User.query.filter_by(email=email).first_or_404()

    if not user.verify_password(password):
        return jsonify({
            'error': 'password'
        }), 403

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'])

    return jsonify({
        'token': token.decode('utf-8')
    })

@app.route('/auth/protected', methods=['GET'])
@jwt_required
def protected(current_user):
    result = users_share_schema.dump(
        User.query.all()
    )
    return jsonify({
        'allUser': result,
        'username': current_user.name
    })



