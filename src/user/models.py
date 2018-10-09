from flask_sqlalchemy import BaseQuery

from core import bcrypt
from core.models import db, TimestampMixin

#################################################
# User model and query set
#################################################

class UserQuery(BaseQuery):
    def get_by_id(self, id):
        return self.get(ident=id)

    def get_by_email(self, email):
        return self.filter_by(email=email).first()


class User(db.Model, TimestampMixin):
    query_class = UserQuery
    id = db.Column(db.Integer, primary_key=True)
    todos = db.relationship('Todo', backref='user', lazy=True)

    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))

    first_name = db.Column(db.Unicode(100))
    last_name = db.Column(db.Unicode(100))

    auth_sub = db.Column(db.String(100))
    notifications_enabled = db.Column(db.Boolean())
    notifications_radius_meters = db.Column(db.Float())
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    expires_at = db.Column(db.DateTime())

    @property
    def password(self):
        raise AttributeError('password is a write only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def create_new_user(cls, data):
        user = User.query.get_by_email(email=data['email'])

        if not user:
            new_user = User(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )

            db.session.add(new_user)
            db.session.commit()
            return new_user