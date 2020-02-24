from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return f"<User : {self.username} >"

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

user_share_schema = UserSchema()
users_share_schema = UserSchema(many=True)