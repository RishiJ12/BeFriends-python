from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
 
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


   


