from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    delete = SubmitField('Delete Task')

class TaskStatusForm(FlaskForm):
    taskstatus = RadioField('Task Status', choices=[('on', 'On'), ('off', 'Off')],default='off',
                                  validators=[DataRequired()])
    confirm = SubmitField('Confirm')

class TaskDescriptionForm(FlaskForm):
    descrip_edit = SubmitField('Edit Description')

class Sen_Plug_EditForm(FlaskForm):
    sen_Plug_edit = SubmitField('Edit Sensors & Plugins')