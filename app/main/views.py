from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User,Task
from . import main
from .forms import NameForm, DeleteForm, TaskStatusForm
from flask import flash
import os


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
         # ...
        return redirect(url_for('.index'))
    return render_template('index.html',
                            form=form, name=session.get('name'),
                            known=session.get('known', False),
                            current_time=datetime.utcnow())

@main.route('/dashboard',methods=['GET', 'POST'])
@login_required
def dashboard():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template('dashboard.html',tasks=tasks)

@main.route('/task/<int:taskid>/<userid>',methods=['GET', 'POST'])
@login_required
def task(taskid,userid):
    #tasks = Task.query.order_by(Task.id.desc()).all()
    task=Task.query.filter(Task.id==taskid).first()
    flash(task.taskname)
    delete_form=DeleteForm()
    taskstatusform = TaskStatusForm()
    if taskstatusform.validate_on_submit():
        #Change broker's status according to radiofield's value.
        flash(taskstatusform.taskstatus.data)
        #os.system('brew services stop mosquitto')
        #os.system('brew services start mosquitto')
    qrcodelink=generate_qrcode(task)
    return render_template('task.html',task=task,delete_form=delete_form,taskstatusform = taskstatusform,qrcodelink=qrcodelink)



#Function for generating the qrcode.
def generate_qrcode(task):
    api = 'https://chart.googleapis.com/chart?'
    #Kind of the pic we need to generate.
    cht='qr'
    #Error toleration rate.
    chld='H'
    #Size of the qr code.
    chs='200x200'
    #Information in the qr code.
    chl='taskid'+str(task.id)+';taskname:'+task.taskname+';taskdescription:'+task.description
    link=api+'cht='+cht+'&chld='+chld+'&chs='+chs+'&chl='+chl
    return link