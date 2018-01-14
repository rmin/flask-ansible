#!/usr/bin/env python

import logging
from ansiblerunner import AnsibleRunner
from application_config import *
from flask import Flask, request, jsonify
app = Flask(__name__)

LOCALLOGS   = True
PRIVATE_KEY = '/etc/ssh/id_rsa_ansible'
REMOTE_USER = 'root'
MODULE_PATH = '/var/www/library'


@app.route("/", methods=['GET'])
def index():
    host = request.form['host'] if 'host' in request.form else request.args.get('host', '')
    # validate input
    if not len(host):
        return jsonify({'success': False, 'msg': 'host is required'})
    # make it work for multiple hosts
    host_list = host.split(",")

    try:
        ansbl = AnsibleRunner(host=host_list, user=REMOTE_USER, key=PRIVATE_KEY, module_path=MODULE_PATH)

        result = ansbl.run([
            dict(action=dict(module='shell', args="hostname -f")),
            dict(action=dict(module='yum', args="name=nano, state=latest"))
        ])

        if LOCALLOGS:
            app.logger.warning(repr(result))

        return jsonify({'success': True, 'msg': result})
        
    except Exception, e:
        return jsonify({'success': False, 'msg': str(e)})


if __name__ == "__main__":
    if LOCALLOGS:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
        app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=80, threaded=True)