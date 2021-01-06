from flask_httpauth import HTTPBasicAuth
from ..models import Task
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(task_id, certificate):
    if task_id == '':
        return False
    #Only accept if the certificate is right for the task.
    task = Task.query.filter_by(id=task_id,certificate=certificate).first()
    if not task:
        return False
    return True

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')