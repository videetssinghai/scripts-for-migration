from flask import Flask
from subprocess import Popen, PIPE
from flask.ext.api import status
import requests
import time
from flask import request
from random import randint 

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
	# client_ip = request.environ['REMOTE_ADDR']
	# print client_ip
	threshold = 50
	print "threshold rtt: "+ str(threshold)
	rtt1 = 10
	print "rtt1: "+str(rtt1)
	while (rtt1<threshold):
		#time.sleep(4)
		rtt1+=15
		print "rtt1: "+ str(rtt1)
	print "rtt1 << threshold rtt\nchecking rtt for cloudlet 2..."
	rtt2 = 100
	print "rtt2: "+ str(rtt2)
	while (rtt2>rtt1):
		rtt1+=15
		rtt2-=10
		print "rtt1: "+ str(rtt1)
		print "rtt2: "+ str(rtt2)
		#time.sleep(4)
	print "rtt2 << rtt1"
	print "Starting Migration to Cloudlet 2...\n\n"
	initm()
	return 'Hello, world!\n'

@app.route('/request')
def request():
	print "Request from 2 recieved"
	return "Request from 2 recieved"

@app.route('/migrate')
def migrate():
	migrateVM()
	return "Migrated"

@app.route('/initmigrate')
def initm():
  result = check()
  if result == True:
    create_vm = requests.get('http://172.16.40.65:5000/init')
    print create_vm.text
    print "Starting VM at Cloudlet 2...."
    start_vm = requests.get('http://172.16.40.65:5000/start')
    print start_vm.text
    time.sleep(4)
    migrate()
    return start_vm.text
  else:
    print "request to server 2 failed at server 2"
    return "request to server 2 failed at server 2"

@app.route('/init')
def initMigrate():
    initVM()
    createMedium()
    createIDE()
    createSATA()
    setTeleporterOn()
    print "VM initialized.."
    return "VM initialized"

def initVM():
    createVM()
    setRAM()
    setVRAM()
    setBridgeAdaptor()
    attachBridgeToNIC()
    setPAE()
    setConfigs()
    setUniversalTime()  

def check():
	r = requests.get('http://172.16.40.65:5000/request')
	if r.status_code == 200:
		return True
	else:
		return False

def migrateVM():
	print "VM Migrating..."
	start_time = time.time()
	p = Popen('VBoxManage controlvm videet_25_1 teleport --host 172.16.40.65 --port 6000', shell=True, stdout=PIPE, stderr=PIPE)
	out, err = p.communicate()
	end_time = time.time()
	print start_time
	print end_time
	print end_time - start_time
	print out
	print err

def setTeleporterOn():
    p = Popen('VBoxManage modifyvm ubuntu --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()


def createVM():
     new_vm = Popen('VBoxManage createvm --name ubuntu --ostype Ubuntu_64 --register', shell=True, stdout=PIPE, stderr=PIPE)
     out, err = new_vm.communicate()
     print out
     print err

def setRAM():
    ram = Popen('VBoxManage modifyvm ubuntu --memory 2048', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = ram.communicate()

def setVRAM():
    vram = Popen('VBoxManage modifyvm ubuntu --vram 16', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = vram.communicate()

def setBridgeAdaptor():
    adaptor = Popen('VBoxManage modifyvm ubuntu --bridgeadapter1 enp1s0', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = adaptor.communicate()

def attachBridgeToNIC():
    nic = Popen('VBoxManage modifyvm ubuntu --nic1 bridged', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = nic.communicate()

def setPAE():
    pae = Popen('VBoxManage modifyvm ubuntu --pae off', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pae.communicate()


def setConfigs():
    #set mouse configs
    mouse = Popen('VBoxManage modifyvm ubuntu --mouse usbtablet', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = mouse.communicate()


    #set usb port off
    usb = Popen('VBoxManage modifyvm ubuntu --usb on', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = usb.communicate()

def setUniversalTime():
    utc = Popen('VBoxManage modifyvm ubuntu --rtcuseutc on', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = utc.communicate()

def createMedium():
    medium = Popen('VBoxManage createmedium --filename /home/itlab/VirtualBox\ VMs/ubuntu2/ubuntu.vdi --diffparent /home/itlab/VMs/ubuntu.vdi --size 8000 --format VDI', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = medium.communicate()
    print out
    print err

def createIDE():
    #create storage controller for IDE
    icontroller = Popen('VBoxManage storagectl ubuntu --name "IDE" --add ide --controller PIIX4', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = icontroller.communicate()


    #attach the storage controller (IDE)
    IDE = Popen('VBoxManage storageattach ubuntu --storagectl "IDE" --port 1 --device 0 --type dvddrive --medium emptydrive', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = IDE.communicate()
 

def createSATA():
    #create storage controller for SATA
    scontroller = Popen('VBoxManage storagectl ubuntu --name "SATA" --add sata --controller IntelAhci --portcount 1', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = scontroller.communicate()


    #attach the storage controller (SATA)
    SATA = Popen('VBoxManage storageattach ubuntu --storagectl "SATA" --port 0 --type hdd --medium /home/itlab/VMs/ubuntu.vdi', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = SATA.communicate()


def startTeleporter():
    teleporter = Popen('VBoxManage modifyvm ubuntu --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = teleporter.communicate()


def startVM():
    VM = Popen('VBoxManage startvm ubuntu', shell=True, stdout=PIPE, stderr=PIPE)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
