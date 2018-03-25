from flask import Flask
from subprocess import Popen, PIPE
from flask.ext.api import status
import requests

app = Flask(__name__)

@app.route('/init')
def hello_world():
    return 'Hello, world!\n'

@app.route('/request1')
def request():
  return status.HTTP_200_OK

@app.route('/migrate')
def migrate():
  result = check()
  if result == True:
    p = Popen('VBoxManage controlvm ubuntu teleport --host 172.16.40.61 --port 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print out
    print err
  else:
    print "request to server 2 failed"

def check():
  r = requests.get('http://172.16.40.61:5000/request2')
  if r.status_code == 200:
    return True
  else:
    return False

if __name__ == '__main__':
    app.run(host='0.0.0.0')
