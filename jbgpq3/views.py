from flask import Flask, request, abort, jsonify
from jbgpq3 import app

import subprocess
import json
import re
import os
import time

@app.route('/')
def index():
    return "fartypants"

@app.route('/prefix/<as_set>')
def get_prefix(as_set):
    if not re.match('^AS', as_set.upper()):
        abort(403, "Doesn't look like an AS-SET or aut-num - otherwise it would begin 'AS'.  ")

    display_prefixlist = {}
    display_prefixlist["as_set"] = as_set

    # IPv4 prefixes
    if os.path.isfile("/tmp/jbgpq3_4" + as_set):
        display_prefixlist["cache_hit"] = True
        filestats = os.stat("/tmp/jbgpq3_4" + as_set)
        display_prefixlist["cache_age_seconds"] = int(time.time() - filestats.st_mtime)
        with open("/tmp/jbgpq3_4" + as_set, "r") as myfile:
            raw_prefixlist = ''.join(myfile.read().splitlines())
    else:
        display_prefixlist["cache_hit"] = False
        display_prefixlist["cache_age_seconds"] = 0
        raw_prefixlist = subprocess.check_output(['bgpq3', '-Aj', as_set])
        with open("/tmp/jbgpq3_4" + as_set, "w") as myfile:
            myfile.write(raw_prefixlist)    
    display_prefixlist["prefixes_ipv4"] = json.loads(raw_prefixlist)["NN"]

    return jsonify(display_prefixlist)