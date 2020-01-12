from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from flask_json import as_json, JsonError,json_response
from werkzeug.security import safe_str_cmp
import ipaddress

from config import *

from shell_utils import *


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/job', methods=['POST'])
# @jwt_required()
@as_json
def post_job():
    if not request.is_json:
        raise JsonError(description='invalid json request',status_=415)
    req = request.get_json()
    try:
        cird_ip = req.get('cidr')
        if not cird_ip:
            raise JsonError(description='invalid input', status_=400)
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='invalid input', status_=400)

    try:
        ipaddress.ip_address(cird_ip)
    except ValueError:
        raise JsonError(description='invalid input value', status_=400)

    if check_cird_detail_sh_running(cird_ip):
        raise JsonError(description='process is running', status_= 420)

    if check_file_exists_for_cird(cird_script_folder,cird_ip):
        return json_response(run_summary_sh(['cd', cird_script_folder, ';', "./summarize-results.sh", 'output-'+cird_ip.replace('/','-')]))

    run_cird_sh(['cd', cird_script_folder, ';', "./CIDRDetail.sh", cird_ip])

    return json_response(run_summary_sh(['cd', cird_script_folder, ';', "./summarize-results.sh", 'output-'+cird_ip.replace('/','-')]))

if __name__ == '__main__':
    app.run()
    
