from flask import Flask
from subprocess import Popen, PIPE
from flask.ext.api import status

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!\n'

@app.route('/request2')
def request():
    return status.HTTP_200_OK

@app.route('/migrate')
def migrate():
    result = check()
    if result == True:
        create_vm = requests.get('http://172.16.40.65:5000/init')
        if create_vm == True:
            migrateVM()
        else:
            print "VM Creation failed at server 1"
    else:
        print "request to server 2 failed"

@app.route('/init')
def initMigrate():
    initVM()
    createMedium()
    createIDE()
    createSATA()
    startTeleporter()
    startVM()
    setTeleporterOn()
    return True

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
  r = requests.get('http://172.16.40.68:5000/request1')
  if r.status_code == 200:
    return True
  else:
    return False

def migrateVM():
    p = Popen('VBoxManage controlvm ubuntu2 teleport --host 172.16.40.68 --port 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print out
    print err

def setTeleporterOn():
    p = Popen('VBoxManage modifyvm ubuntu2 --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print out
    print err

def createVM():
     new_vm = Popen('VBoxManage createvm --name ubuntu2 --ostype Ubuntu_64 --register', shell=True, stdout=PIPE, stderr=PIPE)
     out, err = new_vm.communicate()
     print out
     print err

def setRAM():
    ram = Popen('VBoxManage modifyvm ubuntu2 --memory 2048', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = ram.communicate()
    print out
    print err

def setVRAM():
    vram = Popen('VBoxManage modifyvm ubuntu2 --vram 16', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = vram.communicate()
    print out
    print err

def setBridgeAdaptor():
    adaptor = Popen('VBoxManage modifyvm ubuntu2 --bridgeadapter1 enp1s0', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = adaptor.communicate()
    print out
    print err

def attachBridgeToNIC():
    nic = Popen('VBoxManage modifyvm ubuntu2 --nic1 bridged', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = nic.communicate()
    print out
    print err

def setPAE():
    pae = Popen('VBoxManage modifyvm ubuntu2 --pae off', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pae.communicate()
    print out
    print err

def setConfigs():
    #set mouse configs
    mouse = Popen('VBoxManage modifyvm ubuntu2 --mouse usbtablet', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = mouse.communicate()
    print out
    print err

    #set usb port off
    usb = Popen('VBoxManage modifyvm ubuntu2 --usb on', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = usb.communicate()
    print out
    print err

def setUniversalTime():
    utc = Popen('VBoxManage modifyvm ubuntu2 --rtcuseutc on', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = utc.communicate()
    print out
    print err

def createMedium():
    medium = Popen('VBoxManage createmedium --filename /home/itlab/VirtualBox\ VMs/ubuntu2/ubuntu.vdi --diffparent VMs/ubuntu.vdi --size 8000 --format VDI', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = medium.communicate()
    print out
    print err

def createIDE():
    #create storage controller for IDE
    icontroller = Popen('VBoxManage storagectl ubuntu2 --name "IDE" --add ide --controller PIIX4', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = icontroller.communicate()
    print out
    print err

    #attach the storage controller (IDE)
    IDE = Popen('VBoxManage storageattach ubuntu2 --storagectl "IDE" --port 1 --device 0 --type dvddrive --medium emptydrive', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = IDE.communicate()
    print out
    print err

def createSATA():
    #create storage controller for SATA
    scontroller = Popen('VBoxManage storagectl ubuntu2 --name "SATA" --add sata --controller IntelAhci --portcount 1', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = scontroller.communicate()
    print out
    print err

    #attach the storage controller (SATA)
    SATA = Popen('VBoxManage storageattach ubuntu2 --storagectl "SATA" --port 0 --type hdd --medium /home/itlab/VMs/ubuntu.vdi', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = SATA.communicate()
    print out
    print err

def startTeleporter():
    teleporter = Popen('VBoxManage modifyvm ubuntu2 --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = teleporter.communicate()
    print out
    print err

def startVM():
    VM = Popen('VBoxManage startvm ubuntu2', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = VM.communicate()
    print out
    print err

if __name__ == '__main__':
    app.run(host='0.0.0.0')
