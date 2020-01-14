import subprocess


sanitized_cird = "mysql".replace('/', '-')
docker_name = subprocess.run([
                          f'docker ps -qf "name={sanitized_cird}"'],
                      shell=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8')

if docker_name:
    print('presnet')
else:
    print('not')