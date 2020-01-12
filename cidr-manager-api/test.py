import subprocess

comms = ['cd', 'cird_script_folder', ';', "./CIDRDetail.sh", 'cird_ip']

p = subprocess.Popen(comms, shell=True,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
if not p.poll():
    print('here')
    print(p.stderr.read().decode('utf-8'))
