import os
import ast
import requests
from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User,Task
from . import main
from .forms import NameForm, DeleteForm, TaskStatusForm, TaskDescriptionForm, Sen_Plug_EditForm
from flask import flash
from .. import mqtt
import pymysql
import json

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
    tasks = Task.query.filter(Task.creator_id==current_user.id).order_by(Task.id.desc()).all()
    return render_template('dashboard.html',tasks=tasks)

@main.route('/task/<int:taskid>/<userid>',methods=['GET', 'POST'])
@login_required
def task(taskid,userid):
    #tasks = Task.query.order_by(Task.id.desc()).all()
    task=Task.query.filter(Task.id==taskid).first()
    delete_form=DeleteForm()
    taskstatusform = TaskStatusForm()
    if(task.task_status == 0):
        taskstatusform.taskstatus.data='off'
    elif(task.task_status == 1):
        taskstatusform.taskstatus.data='on'
        
    description_edit_form = TaskDescriptionForm()
    if taskstatusform.validate_on_submit():
        #Change subscriber's status according to radiofield's value.
        if(taskstatusform.taskstatus.data == 'on'):
            flash("You just turn on the task: "+task.taskname)
            change_task_status(task,1)
            mqtt.subscribe(task.taskname)
            print('subscribe to '+task.taskname)
        elif (taskstatusform.taskstatus.data == 'off'):
            flash("You just turn off the task: "+task.taskname)
            change_task_status(task,0)
            mqtt.subscribe(task.taskname)
            print('unsubscribe '+task.taskname)

    qrcodelink=generate_qrcode(task)
    return render_template('task.html',task=task,delete_form=delete_form,taskstatusform = taskstatusform,description_edit_form=description_edit_form,qrcodelink=qrcodelink)

#Function for generating the qrcode.
def generate_qrcode(task):
    api = 'https://chart.googleapis.com/chart?'
    #Kind of the pic we need to generate.
    cht='qr'
    #Error toleration rate.
    chld='H'
    #Size of the qr code.
    chs='300x300'
    #Information in the qr code.
    sensors_dict=ast.literal_eval(task.sensors)
    server_ip=get_ip()
    chl=server_ip+':5000/api/v1/tasks/'+str(task.id)
    #chl='{"task_id":'+str(task.id)+',"task_name":'+task.taskname+',"task_description":'+task.description+',"task_sensors":'+str(sensors_dict)+',"task_created_at":'+str(task.created_at)+',"task_creator_id":'+str(task.creator_id)+',"task_certificate":'+str(task.certificate)+',"server_ip":'+server_ip+'}'
    link=api+'cht='+cht+'&chld='+chld+'&chs='+chs+'&chl='+chl
    return link

def get_ip():
    response = requests.get("https://api.ipify.org/?format=text")
    ip = response.text

    return ip

def change_task_status(task, task_status):
    task.task_status=task_status
    db.session.add(task)
    db.session.commit()