from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Task
from ..email import send_email
from .forms import LoginForm, RegistrationForm, NewTaskForm
import qrcode
import os
import pymysql
import random

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
                # flash(user.id)
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    password=form.password.data,
                    confirmed=1)
        db.session.add(user)
        db.session.commit()
        #Create a new database for new user.
        create_new_database(user)
        #token = user.generate_confirmation_token()
        #send_email(user.email, 'Confirm Your Account','auth/email/confirm', user=user, token=token)
        flash('You have registered your account. Thanks!')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/new_task', methods=['GET', 'POST'])
@login_required
def new_task():
    form = NewTaskForm()
    if form.validate_on_submit():
        # flash(current_user.firstname)
        sensors = {'camera' : form.camera.data, 'co2' : form.co2.data, 'air_pressure' : form.air_pressure.data, 'motion' : form.motion.data, 'audio' : form.audio.data, 'uv' : form.uv.data, 'humidity' : form.humidity.data, 'temp' : form.temp.data}
        cert=generate_certificate()
        task = Task(taskname=form.taskname.data, description=form.description.data, sensors=str(sensors),creator_id=current_user.id,certificate=cert)
        db.session.add(task)
        db.session.commit()
        flash('A new task just established!')
        #Create a new table in user's database.
        create_new_databasetable(current_user,task)
        return redirect(url_for('main.dashboard'))
    return render_template('auth/newtask.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
    
#Function for creating new user's database.
def create_new_database(user):
    conn = pymysql.connect(host='localhost',user='root',password='han784533',charset='utf8mb4')
    cursor = conn.cursor()
    sql= "CREATE DATABASE IF NOT EXISTS "+user.lastname+"_"+str(user.id)
    cursor.execute(sql)
    sql2="CREATE USER '%s'@'localhost' IDENTIFIED BY 'han784533';"%(user.lastname+"_"+str(user.id))
    cursor.execute(sql2)
    sql3="GRANT Create, Select, Insert, Update, Delete ON %s to '%s'@'localhost';"%(user.lastname+"_"+str(user.id)+".*",user.lastname+"_"+str(user.id))
    cursor.execute(sql3)

#Function for creating user's task table in user's database.
def create_new_databasetable(current_user,task):
    conn =pymysql.connect(host='localhost',user=current_user.lastname+"_"+str(current_user.id),password='han784533',db=current_user.lastname+"_"+str(current_user.id),port=3306)
    cursor = conn.cursor()
    sql = "CREATE TABLE %s (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, client_id INT, receve_time DATETIME, camera varchar(20), temperature varchar(20), humidity varchar(20), co2 varchar(20), air_pressure varchar(20), motion varchar(20), uv varchar(20));"%(task.taskname+"_"+str(task.id))
    #Create data table with all sensors as column.
    cursor.execute(sql)

#Function for generating new certificate for new task.
def generate_certificate():
    cert = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        cert += ch
    return cert