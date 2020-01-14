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
    sanitized_cird = cird_ip.replace('/', '-')
    return subprocess.run([f'docker run -d --rm --network=host -v {cird_script_folder}:/root/bin/NetDetails:rw -w /root/bin/NetDetails --name {sanitized_cird} cidr_runner:latest ./CIDRDetail.sh {cird_ip}'], shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=cird_script_folder).stdout.decode('utf-8')




    # with cd(cird_script_folder):
    #     os.system(f"./CIDRDetail.sh {cird_ip} &")
    #                          # stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # return p


def run_summary_sh(cird_ip):
    # with cd(cird_script_folder):
    return subprocess.run([f"./summarize-results.sh {cird_ip.replace('/', '-')}"], shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=cird_script_folder).stdout.decode('utf-8')


# def check_cird_detail_sh_running(cird_ip):
#     '''
#     Check if there is any running process that contains the given name processName.
#     '''
#     # Iterate over the all the running process
#     for proc in psutil.process_iter():
#         try:
#
#             # Check if process name contains the given name string.
#             cmdline_str = " ".join(proc.cmdline()).lower()
#             if "CIDRDetail.sh".lower() in cmdline_str and cird_ip.lower() in cmdline_str:
#                 return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False;


def check_cird_detail_sh_running(cird_ip):
    sanitized_cird = cird_ip.replace('/', '-')
    docker_name = subprocess.run([
                              f'docker ps -qf "name={sanitized_cird}"'],
                          shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')

    if docker_name:
        return True
    else:
        return False


def get_ip_cidr_file_path(cird_ip):
    return os.path.join(cird_script_folder, 'outputfile-' + cird_ip.replace('/', '-'))

def check_detail_file_exists_for_cird(cird_ip):
    return os.path.exists(get_ip_cidr_file_path(cird_ip))

