from datetime import datetime
from flask_login.mixins import UserMixin
from sqlalchemy.orm import backref
from myapp import db
from myapp import login_manager
#from markdown import markdown

class User(db.Model, UserMixin):
    '''
    Create user database for the purpose of storing user information.
        Parameters:
            db.Model :
            UserMixin: 
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash =db.Column(db.String(128))
    #events = db.relationship('Notes',backref='user',lazy = True)
 #Returns a string as a representation of the object.
    def __repr__(self):
        return f'<{self.id} {self.username}  {self.email}  {self.password_hash}>'
    
class Event(db.Model):
    '''
    Create database to store notes information.
        Parameters:
            db.Model 
    '''
    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(128))
    className = db.Column(db.String(128))
    description = db.Column(db.Text(1256))
    location = db.Column(db.String(128))
    date = db.Column(db.String(128))
    date_created = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)

 #Returns a string as a representation of the object.
    def __repr__(self):
        return f'<{self.eventName}  {self.text} >'
   
@login_manager.user_loader
def load_user(id):
    '''
    load user's id
        Parameters:
                id     
        Returns:
            int (id) : user id
    '''
    return User.query.get(int(id))

