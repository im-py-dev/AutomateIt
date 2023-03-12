from flask_login import UserMixin
from app import db, bcrypt


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer, default=1)
    is_admin = db.Column(db.Integer, default=0)
    name = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    applets = db.relationship(
        "Applet",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True)

    @property
    def pw(self):
        raise AttributeError('password is not a readable attribute')

    @pw.setter
    def pw(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Applet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    triggers = db.relationship('Trigger', backref='applet', lazy=True)
    actions = db.relationship('Action', backref='applet', lazy=True)
    user = db.relationship("User", back_populates="applets")


class Trigger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    applet_id = db.Column(db.Integer, db.ForeignKey('applet.id'), nullable=False)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    applet_id = db.Column(db.Integer, db.ForeignKey('applet.id'), nullable=False)
