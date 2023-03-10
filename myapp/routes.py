
from os import error
from re import S
from flask import escape
from sqlalchemy.orm import session
from werkzeug.security import check_password_hash, generate_password_hash
from myapp import myobj
from myapp import db
from myapp.loginforms import LoginForm
from myapp.deleteforms import DeleteForm
from myapp.models import User
from myapp.registerforms import RegisterForm
from flask import render_template, escape, flash, redirect,request, send_file
from markdown import markdown
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from datetime import datetime
from io import BytesIO
import pdfkit
from werkzeug.utils import secure_filename

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
        email = form.email.data
        password = form.password_hash.data
        user = User.query.filter_by(email=email).first()
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
        return redirect('/home')
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

