from flask import jsonify,request
from ..models import Task, Device
from . import api
from .. import db
from future.backports.urllib import request


@api.route('/tasks/<int:id>/join/',methods=['POST'])
def new_device(id):
    #Register new device for task.
    device = Device.from_json(request.json)
    db.session.add(device)
    db.session.commit()

    #Get task's status
    task = Task.query.get_or_404(id)
    status = task.task_status
    join_result = True
    return jsonify({'join_result':join_result,'device_id':device.id,'task_status':status})

@api.route('/tasks/<int:device_id>/<int:device_status>/update',method=['PUT'])
def update_device_status(device_status):
    device = Device.query.get_or_404(device_id)
    device.device_status = device_status
    db.session.add(device)
    db.session.commit()
    change_result=True
    return jsonify({'change_result':change_result})
