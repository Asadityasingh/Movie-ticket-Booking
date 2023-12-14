from flask_login import UserMixin
from flask_security import RoleMixin
from database import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer,
                                 db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True,
                     default='user', nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'

shows_theatres = db.Table('shows_theatres',
                          db.Column('show_id', db.Integer,
                                    db.ForeignKey('show.id')),
                          db.Column('theatre_id', db.Integer,
                                    db.ForeignKey('theatre.id'))
                          )

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Theatre {self.name}>'

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)
    bookings = db.relationship('Booking', backref='show', lazy=True)
    theatres = db.relationship('Theatre', secondary=shows_theatres,
                            backref=db.backref('shows', lazy='dynamic'))


    def __repr__(self):
        return f'<Show {self.name}>'
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_time = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Booking {self.id}>'