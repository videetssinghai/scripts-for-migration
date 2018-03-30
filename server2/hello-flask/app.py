from flask import Flask
from subprocess import Popen, PIPE
from flask.ext.api import status
import time

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'Hello, world!\n'

@app.route('/request')
def request():
    print "Request from 1 recieved"
    return "Request from 1 recieved"

@app.route('/start')
def start():
    startVM()
    return "VM Started"

@app.route('/migrate')
def migrate():
    migrateVM()
    return "Migrated"

@app.route('/initmigrate')
def initm():
  result = check()
  if result == True:
    create_vm = requests.get('http://172.16.40.68:5000/init')
    return create_vm.text
  else:
    print "request to server 1"
    return "request to server 1"

@app.route('/init')
def initMigrate():
    initVM()
    createMedium()
    createIDE()
    createSATA()
    setTeleporterOn()
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
  r = requests.get('http://172.16.40.68:5000/request')
  if r.status_code == 200:
    return True
  else:
    return False

def migrateVM():
    print "VM Migrating..."
    p = Popen('VBoxManage controlvm ubuntu2 teleport --host 172.16.40.68 --port 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print out
    print err

def setTeleporterOn():
    p = Popen('VBoxManage modifyvm ubuntu2 --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

def createVM():
     new_vm = Popen('VBoxManage createvm --name ubuntu2 --ostype Ubuntu_64 --register', shell=True, stdout=PIPE, stderr=PIPE)
     out, err = new_vm.communicate()
     print out
     print err

def setRAM():
    ram = Popen('VBoxManage modifyvm ubuntu2 --memory 2048', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = ram.communicate()

def setVRAM():
    vram = Popen('VBoxManage modifyvm ubuntu2 --vram 16', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = vram.communicate()


def setBridgeAdaptor():
    adaptor = Popen('VBoxManage modifyvm ubuntu2 --bridgeadapter1 enp1s0', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = adaptor.communicate()


def attachBridgeToNIC():
    nic = Popen('VBoxManage modifyvm ubuntu2 --nic1 bridged', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = nic.communicate()


def setPAE():
    pae = Popen('VBoxManage modifyvm ubuntu2 --pae off', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pae.communicate()


def setConfigs():
    #set mouse configs
    mouse = Popen('VBoxManage modifyvm ubuntu2 --mouse usbtablet', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = mouse.communicate()


    #set usb port off
    usb = Popen('VBoxManage modifyvm ubuntu2 --usb on', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = usb.communicate()


def setUniversalTime():
    utc = Popen('VBoxManage modifyvm ubuntu2 --rtcuseutc on', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = utc.communicate()


def createMedium():
    medium = Popen('VBoxManage createmedium --filename /home/itlab/VirtualBox\ VMs/ubuntu2/videet.vdi --diffparent /home/itlab/VMs/videet.vdi --size 8000 --format VDI', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = medium.communicate()
    print out
    print err

def createIDE():
    #create storage controller for IDE
    icontroller = Popen('VBoxManage storagectl ubuntu2 --name "IDE" --add ide --controller PIIX4', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = icontroller.communicate()


    #attach the storage controller (IDE)
    IDE = Popen('VBoxManage storageattach ubuntu2 --storagectl "IDE" --port 1 --device 0 --type dvddrive --medium emptydrive', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = IDE.communicate()


def createSATA():
    #create storage controller for SATA
    scontroller = Popen('VBoxManage storagectl ubuntu2 --name "SATA" --add sata --controller IntelAhci --portcount 1', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = scontroller.communicate()


    #attach the storage controller (SATA)
    SATA = Popen('VBoxManage storageattach ubuntu2 --storagectl "SATA" --port 0 --type hdd --medium /home/itlab/VMs/videet.vdi', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = SATA.communicate()


def startTeleporter():
    teleporter = Popen('VBoxManage modifyvm ubuntu2 --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = teleporter.communicate()


def startVM():
    VM = Popen('VBoxManage startvm ubuntu2', shell=True, stdout=None, stderr=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
