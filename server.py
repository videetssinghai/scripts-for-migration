from flask import Flask
from subprocess import Popen, PIPE
import requests
import time
from flask import request
import config
import mysql_config

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    # rtt working is simulated
    #code to update cloud to cloud rtt. run ever 120s.
    
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    cur.execute("select IPaddress from neighbour_cloudlets")
    rows=cur.fetchall()

    addrs = [row[0] for row in rows]
    for ip in addrs:
        set_ip = requests.get(getCustomURL(ip, data = client_ip))
        print "rtt to " + ip + " " +set_ip + "\n\n"

    cur.close()                                      
    connection.close()

    #--------------------------

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
    print msg_start_migrate
    initm()
    return 'Hello, world!\n'

@app.route('/request')
def req():
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    msg_request_recieved = "Request from " + client_ip +" recieved"
    print msg_request_recieved
    return msg_request_recieved
    # return request.headers['X-Real-IP']

@app.route('/setIP')
def setIP():
    print "mobile ip: " + str(request.data)
    dir = []
    dir.append(request.data)
    mp = MultiPing(dir)
    mp.send()
    responses, no_responses = mp.receive(0.01)
    addr, rtt = responses.items()
    return rtt

def getCustomURL(IPaddress):
    return 'http://' + IPaddress + ':5000/set_ip'


@app.route('/start')
def start():
    startVM()
    return msg_vm_start

@app.route('/migrate')
def migrate():
    migrateVM()
    return msg_migrated

@app.route('/initmigrate')
def initm():
  result = check()
  if result == True:
    create_vm = requests.get(getURL('init'))
    print create_vm.text
    print msg_vm_starting
    start_vm = requests.get(getURL('start'))
    print start_vm.text
    time.sleep(4)
    migrate()
    return start_vm.text
  else:
    print msg_request_failed
    return msg_request_failed

@app.route('/init')
def initMigrate():
    initVM()
    createMedium()
    time.sleep(1)
    createIDE()
    createSATA()
    setTeleporterOn()
    return msg_vm_setup

def initVM():
    createVM()
    setRAM()
    setCpu()
    setCap()
    setVRAM()
    setBridgeAdaptor()
    attachBridgeToNIC()
    setPAE()
    setConfigs()
    setUniversalTime()

def check():
    r = requests.get(getURL('request'))
    if r.status_code == 200:
        return True
    else:
        return False

def getURL(route):
    return 'http://' + target_host + ':5000/' + route

def migrateVM():
    print "VM Migrating..."
    start_time = time.time()
    p = Popen('VBoxManage controlvm ' + vm_name + ' teleport --host ' + target_host + ' --port 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    end_time = time.time()    
    print start_time
    print end_time
    print end_time - start_time
    print out
    print err


def setTeleporterOn():
    p = Popen('VBoxManage modifyvm ' + vm_name + ' --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

def createVM():
    new_vm = Popen('VBoxManage createvm --name ' + vm_name + ' --ostype Ubuntu_64 --register', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = new_vm.communicate()
    print out
    print err

def setCpu():
    ref_cpu = Popen('VBoxManage modifyvm ' + vm_name + ' --cpus ' + cpu, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = ref_cpu.communicate()

def setCap():
    ref_cap = Popen('VBoxManage modifyvm ' + vm_name + ' --cpuexecutioncap ' + cpu_cap, shell=True, stdout=PIPE, stderr=PIPE)
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
    medium = Popen('VBoxManage createmedium --filename ' + vdi_path + ' --diffparent ' + shared_path + ' --size ' + storage + ' --format VDI', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = medium.communicate()
    print out
    print err

def createIDE():
    #create storage controller for IDE
    icontroller = Popen('VBoxManage storagectl ' + vm_name + ' --name "IDE" --add ide --controller PIIX4', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = icontroller.communicate()


    #attach the storage controller (IDE)
    IDE = Popen('VBoxManage storageattach ' + vm_name + ' --storagectl "IDE" --port 1 --device 0 --type dvddrive --medium emptydrive', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = IDE.communicate()


def createSATA():
    #create storage controller for SATA
    scontroller = Popen('VBoxManage storagectl ' + vm_name + ' --name "SATA" --add sata --controller IntelAhci --portcount 1', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = scontroller.communicate()


    #attach the storage controller (SATA)
    SATA = Popen('VBoxManage storageattach ' + vm_name + ' --storagectl "SATA" --port 0 --type hdd --medium '+ shared_path, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = SATA.communicate()


def startTeleporter():
    teleporter = Popen('VBoxManage modifyvm ' + vm_name + ' --teleporter on --teleporterport 6000', shell=True, stdout=PIPE, stderr=PIPE)
    out, err = teleporter.communicate()


def startVM():
    VM = Popen('VBoxManage startvm ' + vm_name, shell=True, stdout=None, stderr=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
