from flask import Flask
from subprocess import Popen, PIPE
from flask.ext.api import status
import time

app = Flask(__name__)
app.debug = True

vm_name = 'ubuntu2'
ram = '1024'
cpus = '5'
cpu_cap = '25'
vdi_name = 'videet_25_1.vdi'
vdi_path = '/home/itlab/VirtualBox\ VMs/' +vm_name + '/' + vdi_name
shared_path = '/home/itlab/VMs/' +vdi_name
target_host = '172.16.40.68'
storage = '8000'


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
    create_vm = requests.get('http://' + target_host + ':5000/init')
    return create_vm.text
  else:
    print "request to server 1"
    return "request to server 1"

@app.route('/init')
def initMigrate():
    initVM()
    createMedium()
    time.sleep(1)
    createIDE()
    createSATA()
    setTeleporterOn()
    return "VM setup completed"

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
    p = Popen('VBoxManage controlvm ' + vm_name ' teleport --host' + target_host + ' --port 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print out
    print err

def setTeleporterOn():
    p = Popen('VBoxManage modifyvm ' + vm_name ' --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

def createVM():
    new_vm = Popen('VBoxManage createvm --name ' + vm_name + ' --ostype Ubuntu_64 --register', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = new_vm.communicate()
    print out
    print err

def setCpu():
    ref_cpu = Popen('VBoxManage modifyvm ' + vm_name + ' --cpu ' + cpu, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = ref_cpu.communicate()

def setCap():
    ref_cap = Popen('VBoxManage modifyvm ' + vm_name + ' --cpu ' + cpu_cap, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = ref_cap.communicate()

def setRAM():
    ref_ram = Popen('VBoxManage modifyvm ' + vm_name + ' --memory ' + ram, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = ref_ram.communicate()

def setVRAM():
    vram = Popen('VBoxManage modifyvm ' + vm_name + ' --vram 16', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = vram.communicate()


def setBridgeAdaptor():
    adaptor = Popen('VBoxManage modifyvm ' + vm_name + ' --bridgeadapter1 enp1s0', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = adaptor.communicate()


def attachBridgeToNIC():
    nic = Popen('VBoxManage modifyvm ' + vm_name + ' --nic1 bridged', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = nic.communicate()


def setPAE():
    pae = Popen('VBoxManage modifyvm ' + vm_name + ' --pae off', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pae.communicate()


def setConfigs():
    #set mouse configs
    mouse = Popen('VBoxManage modifyvm ' + vm_name + ' --mouse usbtablet', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = mouse.communicate()


    #set usb port off
    usb = Popen('VBoxManage modifyvm ' + vm_name + ' --usb on', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = usb.communicate()


def setUniversalTime():
    utc = Popen('VBoxManage modifyvm ' + vm_name + ' --rtcuseutc on', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = utc.communicate()


def createMedium():
    medium = Popen('VBoxManage createmedium --filename ' + vdi_path + '--diffparent ' + shared_path + ' --size ' + storage + ' --format VDI', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = medium.communicate()
    print out
    print err

def createIDE():
    #create storage controller for IDE
    icontroller = Popen('VBoxManage storagectl ' + vm_name + '--name "IDE" --add ide --controller PIIX4', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = icontroller.communicate()


    #attach the storage controller (IDE)
    IDE = Popen('VBoxManage storageattach ' + vm_name + '--storagectl "IDE" --port 1 --device 0 --type dvddrive --medium emptydrive', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = IDE.communicate()


def createSATA():
    #create storage controller for SATA
    scontroller = Popen('VBoxManage storagectl ' + vm_name + '--name "SATA" --add sata --controller IntelAhci --portcount 1', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = scontroller.communicate()


    #attach the storage controller (SATA)
    SATA = Popen('VBoxManage storageattach ' + vm_name + '--storagectl "SATA" --port 0 --type hdd --medium '+ shared_path, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = SATA.communicate()


def startTeleporter():
    teleporter = Popen('VBoxManage modifyvm ' + vm_name + '--teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = teleporter.communicate()


def startVM():
    VM = Popen('VBoxManage startvm' + vm_name, shell=True, stdout=None, stderr=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
