vm_name = 'ubuntu2'
ram = '512'
cpu = '5'
cpu_cap = '50'
v_name = 'ubuntu_50_500'
vdi_name = v_name + '.vdi'
vdi_path = '/home/itlab/VirtualBox\ VMs/' +vm_name + '/' + vdi_name
shared_path = '/home/itlab/VMs/'+ v_name + '/' + vdi_name
target_host = '172.16.40.68'
storage = '8000'

msg_request_failed = "Request to " + str(target_host) + " failed"
msg_start_migrate = "Starting Migration to Cloudlet " + str(target_host) + "...\n\n"
msg_migrated = "VM Migrated Successfully!!!!"
msg_vm_start = "Virtual Machine " + str(vm_name) + " at "+ target_host+" started"
msg_vm_starting = "Virtual Machine " + str(vm_name) + " at "+ target_host + " starting..."
msg_vm_setup = "Virtual Machine " + str(vm_name) + " at "+ target_host + " setup completed"