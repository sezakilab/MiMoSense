from flask import jsonify
from ..models import Task
from . import api

#Get task's status
@api.route('/tasks/<int:id>/status/')
def get_task_status(id):
    task = Task.query.get_or_404(id)
    status = task.task_status
    return jsonify({'status':status})