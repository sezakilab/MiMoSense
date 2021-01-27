from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    firstname = StringField('Firstname', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
               'Firstname must have only letters, numbers or '
               'underscores')])
    lastname = StringField('Lastname', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
               'Lastname must have only letters, numbers or '
               'underscores')])          
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    #Create new database for new user.
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class NewTaskForm(FlaskForm):
    taskname = StringField('Taskname', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
               'Taskname must have only letters, numbers or '
               'underscores')])
    description = StringField('Description', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9 ,._]*$', 0,
               'Description must have only letters, numbers, space or '
               'underscores')])
    #sensors_text =TextField('Sensors')
    camera =BooleanField('Camera')
    co2 =BooleanField('Co2')
    air_pressure =BooleanField('Air Pressure')
    motion =BooleanField('Motion')
    audio =BooleanField('Audio')
    uv =BooleanField('UV')
    humidity =BooleanField('Humidity')
    temp = BooleanField('Temperature')

    confirm = SubmitField('Confirm')

    #generate_qrcode = SubmitField('Generate QRcode')
    
    