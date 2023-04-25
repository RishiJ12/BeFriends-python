from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
class DeleteForm(FlaskForm):
    '''
    Create form filed for the purpose of delete account information.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password',validators=[DataRequired()])
    delete = SubmitField('Submit')

class DeleteEventForm(FlaskForm):
    '''
    Create form filed for the purpose of delete account information.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    delete = SubmitField('Delete')

class EventForm(FlaskForm):
    '''
    Create form filed for the purpose of login account information.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    eventName = StringField('Event Name', validators=[DataRequired()])
    className = StringField('Class Name', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create')

class LoginForm(FlaskForm):
    '''
    Create form filed for the purpose of login account information.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    username = StringField('Username', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password',validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    '''
    Create form filed for the purpose of signing up account information.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    username = StringField('Username', validators=[DataRequired()])
    password_hash = PasswordField('Password',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    register = SubmitField('Sign up')

class JoinNowForm(FlaskForm):
    join = SubmitField("Join Now")
    