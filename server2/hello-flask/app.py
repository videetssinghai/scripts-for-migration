from flask import Flask
from subprocess import Popen, PIPE
from flask.ext.api import status

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!\n'

@app.route('/init')
def initVM():
	p = Popen('VM creation script', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print out
    print err

@app.route('/request2')
     return status.HTTP_200_OK

@app.route('/migrate')
def migrate():
	p = Popen('VBoxManage modifyvm ubuntu --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print out
    print err

if __name__ == '__main__':
    app.run(host='0.0.0.0')
