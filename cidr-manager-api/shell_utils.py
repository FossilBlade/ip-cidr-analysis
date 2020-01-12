import psutil
import os
import subprocess
from config import *

class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def run_cird_sh(cird_ip):
    with cd(cird_script_folder):
        p = subprocess.Popen([f"./CIDRDetail.sh {cird_ip}"], shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # if p.stdout:
    #     print('here')
    #     print(p.stdout.read().decode('utf-8'))
    # if p.stderr:
    #     print('there')
    #     print(p.stderr.read().decode('utf-8'))
    return p


def run_summary_sh(cird_ip):
    with cd(cird_script_folder):
        return subprocess.run([f"./summarize-results.sh {cird_ip.replace('/', '-')}"], shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')


def check_cird_detail_sh_running(cird_ip):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:

            # Check if process name contains the given name string.
            cmdline_str = " ".join(proc.cmdline()).lower()
            if "CIDRDetail.sh".lower() in cmdline_str and cird_ip.lower() in cmdline_str:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


def check_file_exists_for_cird(folder, cird_ip):
    return os.path.exists(os.path.join(folder, 'outputfile-' + cird_ip.replace('/', '-')))

