from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
mqtt=Mqtt()
socketio = SocketIO()

login_manager = LoginManager()
login_manager.login_view = 'auth.login' 


def create_app(config_name):
    app = Flask(__name__)
    # Configure the MQTT client
    app.config['MQTT_BROKER_URL'] = 'localhost'  
    app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
    app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
    app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
    app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
    app.config['MQTT_REFRESH_TIME'] = 1.0 
    app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
    #Use for socketIO.
    #app.config['SECRET_KEY'] = 'secret!'

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mqtt.init_app(app)
    #mqtt.subscribe('test')
    socketio.init_app(app)
    #socketio.run(app,debug=True,host='0.0.0.0',port=5000)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    
    return app
