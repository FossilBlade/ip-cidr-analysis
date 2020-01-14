from flask import Flask, request, send_file
from flask_jwt import JWT, jwt_required, current_identity
from flask_json import FlaskJSON, as_json, JsonError, json_response
from werkzeug.security import safe_str_cmp
import ipaddress
import logging
import datetime
from shell_utils import *

from flask_cors import CORS

log = logging.getLogger(__name__)

from user_db import users

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__,)
app.debug = True
app.config["APPLICATION_ROOT"] = "/api"
app.config['SECRET_KEY'] = '53453453535sdfsdfsafasdf8asdfsdafsadf56asdfadsfdsfasdf'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=30)

FlaskJSON(app)

jwt = JWT(app, authenticate, identity)
app.config['CORS_ENABLED'] = True
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     supports_credentials=True)


@app.route('/job')
@jwt_required()
@as_json
def run_job():

    print(request.args)
    try:
        cird_ip = request.args['ipcidr']

        if not cird_ip:
            raise JsonError(error='Empty IP provided in request.', status_=400)

        print(cird_ip)
    except (KeyError, TypeError, ValueError):
        raise JsonError(error='IP Not present in request', status_=400)

    try:
        ipaddress.ip_network(cird_ip,False)
    except ValueError as e:
        print(e)
        raise JsonError(error='IP not Valid', status_=400)

    if check_cird_detail_sh_running(cird_ip):
        raise JsonError(error='Process is already running for the given IP', status_=400)

    if check_detail_file_exists_for_cird(cird_ip):
        return dict(result=run_summary_sh(cird_ip))
    try:
        docker_id = run_cird_sh(cird_ip)
        log.info(f'Started docker for {cird_ip} - {docker_id}')
    except:
        log.exception('Error Running Job for IP: '+cird_ip)
        raise JsonError(error='Error running the job for IP. Please check with admin.', status_=500)

    return dict(result='Process initiated for IP. Check back later for the reports.')


@app.route('/report', methods=['HEAD'])
def head_report():
    return {}

@app.route('/report', methods=['GET'])
@jwt_required()
def get_report():
    ip_cidr = request.args.get('ipcidr')

    file_exists = check_detail_file_exists_for_cird(ip_cidr)

    if file_exists:
        return send_file(get_ip_cidr_file_path(ip_cidr),
                         mimetype='text/plain',
                         attachment_filename=f'{ip_cidr.replace("/", "-")}_report.txt',
                         as_attachment=True)
    else:
        raise JsonError(error="Detail report not present for given IP", status_=404)


@app.route('/check')
@jwt_required()
@as_json
def check_ip():
    ip_cidr = request.args.get('ipcidr')

    job_running = check_cird_detail_sh_running(ip_cidr)
    file_exists = check_detail_file_exists_for_cird(ip_cidr)
    summary = None
    if not job_running and file_exists:
        summary = run_summary_sh(ip_cidr)

    return dict(ipcidr=ip_cidr,detail_file_exits=check_detail_file_exists_for_cird(ip_cidr),
            job_running=check_cird_detail_sh_running(ip_cidr),
            summary=summary)

    # return dict(detail_file_exits=True, status_=200,
    #             job_running=False,
    #             summary="hellowsFSFSDFADSFDSFDSFDSFSDFDSAFDSFSDFSDFDSFSDFSDAFDSFSDAF\nASDFADSFADSFSDAFSDFSDAFSDAFDSAFSDAFDSAFDSAFASDF\nasdfdsfdsfdsfdsfsdfdsfdsfdsafadsfdasfdasdaf\nasfdssdfadsfsda\nnasfdasfasdfdsafsdafsdafasdfasd\nasdfadsfasdfsadfasdfsdafadsfasdfasdf\nasdfadsdsafadsfasdfasdfasdfadsdsaf\nafdasdfasdfasdfADFDASFSDFworld".splitlines())


if __name__ == '__main__':
    app.run()
