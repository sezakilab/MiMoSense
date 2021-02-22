from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
import os
from app.exceptions import ValidationError


class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), unique=False, nullable=True)
    lastname = db.Column(db.String(50), unique=False, nullable=True)
    email = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(), unique=False, nullable=True,default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), unique=False, nullable=True,default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task',backref='creator',lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.firstname

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def ping(self):
        self.last_seen =datetime.utcnow()
        db.session.add(self)
        db.session.commit()

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    taskname = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(50), unique=False, nullable=True)
    sensors = db.Column(db.String(255), unique=False, nullable=True)
    plugins = db.Column(db.String(255), unique=False, nullable=True)
    created_at = db.Column(db.DateTime(), unique=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(255), unique=False, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_status = db.Column(db.Integer,unique=False, default=0 )
    delete_status = db.Column(db.Integer,unique=False, default=0 )
    certificate = db.Column(db.String(10), unique=False, nullable=True)
    upload_frequency = db.Column(db.Integer,unique=False, default=1 )

    def __repr__(self):
        return '<Task %r>' % self.taskname

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    device_ip = db.Column(db.String(50), unique=False, nullable=False)
    device_kind = db.Column(db.String(50), unique=False, nullable=False)
    #device_name = db.Column(db.String(50), unique=False, nullable=True)
    created_time = db.Column(db.DateTime(), unique=False,default=datetime.utcnow)
    #device_status = db.Column(db.Integer,unique=False, default=0 )
    
    @staticmethod
    def from_json(json_device):
        device = json_device.get('device_ip')
        if device is None or device == '':
            raise ValidationError('device does not have a body')
        return Device(device=device)
