from datetime import datetime
from flask_login.mixins import UserMixin
from sqlalchemy.orm import backref

from os import error
from re import S
from flask import escape
from sqlalchemy.orm import session
from werkzeug.security import check_password_hash, generate_password_hash

from form import LoginForm,DeleteForm,DeleteEventForm,EventForm,RegisterForm, JoinNowForm
from flask import render_template, escape, flash, redirect,request, send_file
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from io import BytesIO
from flask import Flask
import os
basedir = os.path.abspath(os.path.dirname(__file__))
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor


# create Flask class object named myobj
myobj = Flask(__name__,static_url_path="", static_folder="static")
ckeditor =  CKEditor(myobj)

# Flask login manager
login_manager = LoginManager()
login_manager.init_app(myobj)
login_manager.login_view = 'login'


myobj.config.from_mapping(
    SECRET_KEY = 'you-will-know',
    # location of sqlite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    
)

db = SQLAlchemy(myobj)
migrate = Migrate(myobj,db)
with myobj.app_context():
    db.create_all()


#routes

@myobj.route("/")
def home():
    """Return home page 
    """
    return render_template("home.html")

@myobj.route("/home")
def study():
    """
        Return home page (should be in html)
    """
    return render_template("home.html")

@myobj.route("/login", methods=['GET', 'POST'])
def login(): 
    '''
    Get the login in information from the login page and verify if the 
    information matching the exiting User database. If so log user in.
    otherwise, giving user warning message.
        Returns:
            return html pages
    '''
    form = LoginForm()
    # if the user hit submit on the forms page
    if form.validate_on_submit():
        #email = form.email.data
        username = form.username.data
        password = form.password_hash.data
        user = User.query.filter_by(username = username).first()
        if user != None:
            passed = check_password_hash(user.password_hash,password)
            if passed == True:
                login_user(user)
                flash("Login Successfully!")
            else: 
                flash("Wrong information, please try again")
        else:
            flash('User doesn not exit, try agian!')
            return redirect('/login')
        return redirect('/event')
    return render_template('login.html',form=form)

@myobj.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    '''
    Logout current user and block user from login required page
        Returns:
            return login html page
    '''
    logout_user()
    flash('Logout Successfully!')
    return redirect('/login')


@myobj.route("/register", methods=['GET', 'POST'])
def register():
    '''
    Get the sign up information from the sign up page and store them
    to the User database. Verify the sign up email if already exit, if
    so, flash message to user that email already exiting, otherwise add
    the new user information to the User database
        Returns:
            return html pages
    '''
    form = RegisterForm()
    if form.validate_on_submit():
        #flash(f'{form.username.data} registered succesfully')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password_hash']
            password_hash = generate_password_hash(password)
            email = request.form['email']
            domain = email.split('@')[1]
            if domain == "sjsu.edu":
                if User.query.filter_by(email=email).first():
                    flash('Email already exsit')
                else:
                    add_user = User(username=username,email=email, password_hash=password_hash)
                    db.session.add(add_user)
                    db.session.commit()
                    flash(f'{form.username.data} registered succesfully')
                    return redirect('/login')
            else:
                flash('Plese sign up with your SJSU email')
        
    return render_template('/register.html', form = form)

@myobj.route('/createEvent/', methods=['GET', 'POST'])
@login_required
def createEvent():
    form = EventForm()
    eventname = ""
    if form.validate_on_submit():
        #flash(f'{form.username.data} registered succesfully')
        if request.method == 'POST':
            eventName = request.form['eventName']
            className = request.form['className']
            date = request.form['date']
            description = request.form['description']
            location = request.form['location']
            current = datetime.now()
            add_event = Event(eventName=eventName,className=className, description=description,location = location,date=date,date_created = current,user_id = current_user.id,)
            db.session.add(add_event)
            db.session.commit()
            return redirect('/event')
            
    return render_template('/createEvent.html', form = form)
@myobj.route("/event", methods=['GET', 'POST'])
@login_required
def event_dashboard():
    
    #form = SearchForm()
    note_id = None
    eventname = ""
    date = ""
    description = ""
    location = ""
    events = Event.query.all()
    for event in events:
        #note_id = note.user_id
        eventname = event.eventName
        date = event.date
        description = event.description
        location = event.location
    return render_template('event.html',events=events)



@myobj.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete_account():
    '''
    Get the delete information from the delete page and verify if the 
    information matching the exiting User database and if the user are
    in their own account. If so delete the current user from the database.
    otherwise, giving user warning message.
        Returns:
            return html pages
    '''
    form = DeleteForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        user = User.query.filter_by(email=email).first()
        passed = check_password_hash(user.password_hash,password) 
        if user.id == current_user.id and passed == True:   
            try:
                db.session.delete(user)
                db.session.commit()
                flash('Account Deleted Successfully!')
            except:
                flash('Something went wrong, please try agian later')
        else: 
            flash('Wrong Information, Please Try Agian!')
            return redirect('/delete')
    return render_template('/delete.html', form = form)
@myobj.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('/dashboard.html')



# models
class User(db.Model, UserMixin):
   
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash =db.Column(db.String(128))
    def __repr__(self):
        return f'<{self.id} {self.username}  {self.email}  {self.password_hash}>'
    
class Event(db.Model):
   
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
    
    return User.query.get(int(id))

