from app import db,login
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin,db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True, nullable = False)
    password = db.Column(db.String(64), nullable = False)

    def __repr__(self):
        return '<Usuário {}>'.format(self.username)
    
    def check_password(self, password):
        if self.password == password: 
            return True 
        return False

class Event(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(32), nullable = False)
    description = db.Column(db.String(128))
    date_start = db.Column(db.DateTime, index = True, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    event_owner = db.Column(db.Integer, db.ForeignKey('user.id') )

    def __repr__(self):
        return '<Evento {}>'.format(self.title)

class RelationUsers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'))



class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'))

    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
