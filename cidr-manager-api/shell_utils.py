import psutil
import os
import subprocess

def run_cird_sh(comms):
    p = subprocess.Popen(comms, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p

def run_summary_sh(comms):
    return subprocess.run(comms, stdout=subprocess.PIPE).stdout.decode('utf-8')

def check_cird_detail_sh_running(cird_ip):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            print(proc.cmdline())
            # Check if process name contains the given name string.
            if cird_ip.lower() in proc.cmdline():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


def check_file_exists_for_cird(folder,cird_ip):
    if os.path.exists(os.path.join(folder,'output-'+cird_ip.replace('/','-'))):
        return True
    else:
        return False
