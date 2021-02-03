import os
import click
from app import create_app, db, mqtt
from app.models import User, Task
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

tasks = Task.query.filter(Task.task_status==1).all()
for index in range(len(tasks)):
    mqtt.subscribe(str(tasks[index].id)+'_'+tasks[index].taskname)
    print('subscribe to '+str(tasks[index].id)+'_'+tasks[index].taskname)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Task=Task)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)