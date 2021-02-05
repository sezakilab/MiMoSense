from flask import jsonify,request
from ..models import User,Task, Device
from app import create_app
import os
from .. import mqtt
from . import api
from .. import db
import json
import pymysql
import requests
import time

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()

def get_ip():
    response = requests.get("https://api.ipify.org/?format=text")
    ip = response.text

    return ip

@api.route('/tasks/<int:taskid>',methods=['GET','POST'])
def show_task_info(taskid):
    task = Task.query.filter(Task.id==taskid).first()
    server_ip=get_ip()
    return jsonify({"task_id":task.id,"task_name":task.taskname,"task_description":task.description,"task_sensors":task.sensors,"task_created_at":task.created_at,"task_creator_id":task.creator_id,"task_certificate":task.certificate,"server_ip":server_ip})

@api.route('/tasks/join/',methods=['POST'])
def new_device():
    #Register new device for task.
    #task_id,task_certificate,device_ip,device_kind
    #device = Device.from_json(request.json)
    task_id = request.json.get('task_id')
    task_certificate =request.json.get('task_certificate')
    device_ip =request.json.get('device_ip')
    device_kind =request.json.get('device_kind')
    print(task_id)
    print(task_certificate)
    print(device_ip)
    print(device_kind)
    #Check task's certificate right or not.
    #Need to check device's ip exist or not, if exist, then can not add anymore.
    created_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    device = Device(task_id=task_id,device_ip=device_ip,device_kind=device_kind,created_time=created_time)
    db.session.add(device)
    db.session.commit()

    #Get task's status
    task = Task.query.get_or_404(task_id)
    status = task.task_status
    join_result = True
    return jsonify({'join_result':join_result,'device_id':device.id,'task_status':status})

@api.route('/tasks/<int:device_id>/<int:device_status>/update',methods=['PUT'])
def update_device_status(device_id,device_status):
    device = Device.query.get_or_404(device_id)
    device.device_status = device_status
    db.session.add(device)
    db.session.commit()
    change_result=True
    return jsonify({'change_result':change_result})

@mqtt.on_message()
def handle_mqtt_message(client,userdata, message):
    print("message get!")
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    #socketio.init_app(app)
    #socketio.emit('mqtt_message',data=data)
    print(str(data['payload']))
    #write the data into the database.
    with app.app_context():
        data_json = json.loads(str(data['payload']))
        task_name = data_json['task_name']
        task_id = data_json['task_id']
        creator_id = data_json['creator_id']
        #client_id = data_json['client_id']
        
        #client_ip = data_json['client_ip']
        temperature = data_json['temperature']
        humidity = data_json['humidity']
        co2 = data_json['co2']
        air_pressure = data_json['air_pressure']
        motion = data_json['motion']
        gps = data_json['gps']
        uv = data_json['uv']

        user = User.query.filter(User.id==creator_id).first()

        conn =pymysql.connect(host='localhost',user=user.lastname+"_"+str(user.id),password='han784533',db=user.lastname+"_"+str(user.id),port=3306)
        cursor = conn.cursor()
        upload_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = "INSERT INTO %s VALUES (NULL,1,'%s','camera','%s','%s','%s','%s','%s','%s','%s');" %(task_name+"_"+str(task_id),upload_time,temperature,humidity,co2,air_pressure,motion,gps,uv)
        print(sql)
        cursor.execute(sql)
        cursor.connection.commit()
        print("Just wrote to database!")
        #Flash the data on the html.