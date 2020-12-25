from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User,Task
from . import main
from .forms import NameForm
from flask import flash


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
    return render_template('task.html',task=task)


#Function for generating the qrcode.
def generate_qrcode():
    qr = qrcode.QRCode(
        version =1,
        error_correction= qrcode.constants.ERROR_CORRECT_L,
        box_size = 10,
        border = 4,
    )
    qr.add_data('all_infomation_here')
    qr.make(fit=True)
    qrcode_img=qr.make_image(fill_color="black", back_color="white")
    qrcode_img.save('code_location')
    return 