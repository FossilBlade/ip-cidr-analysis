from flask import Flask, request, send_file
from flask_jwt import JWT, jwt_required, current_identity
from flask_json import FlaskJSON, as_json, JsonError, json_response
from werkzeug.security import safe_str_cmp
import ipaddress

from shell_utils import *

from flask_cors import CORS
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'test', 'test'),
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

FlaskJSON(app)

jwt = JWT(app, authenticate, identity)
app.config['CORS_ENABLED'] = True
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)

@app.route('/job')
@jwt_required()
@as_json
def post_job():
    req = request.get_json(force=True)
    print(req)
    try:
        cird_ip = req.get('ip_cidr')

        if not cird_ip:
            raise JsonError(description='invalid input', status_=400)
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='invalid request type', status_=400)

    try:
        ipaddress.ip_network(cird_ip)
    except ValueError:
        raise JsonError(description='not a valid input value', status_=400)

    if check_cird_detail_sh_running(cird_ip):
        raise JsonError(description='process is running', status_=420)

    if check_file_exists_for_cird(cird_ip):
        return dict(result=run_summary_sh(cird_ip))

    run_cird_sh(cird_ip)

    return dict(result='process started')


@app.route('/report')
@jwt_required()
def get_report():
    ip_cidr = request.args.get('ip_cidr')
    type = int(request.args.get('type'))

    file_exists = check_file_exists_for_cird(ip_cidr)

    if type==0 and file_exists:
        json_response(result="available")


    if file_exists:
        return send_file(get_ip_cidr_file_path(ip_cidr),
                         mimetype='text/plain',
                         attachment_filename=f'{ip_cidr.replace("/", "-")}_detail_report.txt',
                         as_attachment=True)
    else:
        return json_response(result="invalid input",status_=402)

if __name__ == '__main__':
    app.run()
