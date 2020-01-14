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
    dok_comd = f'docker run -d --rm --network=host -v {cird_script_folder}:/root/bin/NetDetails:rw -w /root/bin/NetDetails --name {sanitized_cird} cidr_runner:latest ./CIDRDetail.sh {cird_ip}'

    docker_name = subprocess.run([dok_comd],
                                 shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')

    return docker_name


def run_summary_sh(cird_ip):
    return subprocess.run([f"./summarize-results.sh {cird_ip.replace('/', '-')}"], shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cird_script_folder).stdout.decode('utf-8')


def check_cird_detail_sh_running(cird_ip):
    sanitized_cird = cird_ip.replace('/', '-')
    dok_comd = f'docker ps -qf "name={sanitized_cird}"'
    docker_name = subprocess.run([dok_comd],
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
