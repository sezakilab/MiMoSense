from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,InputRequired
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
    upload_frequency = IntegerField('Upload Frequency (in second, number only)',validators=[InputRequired()])
    
    motion =BooleanField('Motion')
    motion_frequency = IntegerField('Motion Frequency',validators=[InputRequired()])

    temp = BooleanField('Temperature')
    temp_frequency = IntegerField('Temperature Frequency',validators=[InputRequired()])

    humidity =BooleanField('Humidity')
    humidity_frequency = IntegerField('Humidity Frequency',validators=[InputRequired()])

    helmet = BooleanField('Helmet Motion')
    helmet_frequency = IntegerField('Helmet Motion Frequency',validators=[InputRequired()])

    uv =BooleanField('UV')
    uv_frequency = IntegerField('UV Frequency',validators=[InputRequired()])

    camera =BooleanField('Camera')
    camera_frequency = IntegerField('Camera Frequency',validators=[InputRequired()])
    
    co2 =BooleanField('Co2')
    co2_frequency = IntegerField('Co2 Frequency',validators=[InputRequired()])
    
    air_pressure =BooleanField('Air Pressure')
    air_pressure_frequency = IntegerField('Air Pressure Frequency',validators=[InputRequired()])

    audio =BooleanField('Audio')
    audio_frequency = IntegerField('Audio Frequency',validators=[InputRequired()])

    confirm = SubmitField('Confirm')

    #generate_qrcode = SubmitField('Generate QRcode')
    