from flask import Flask, request, abort, jsonify
from jbgpq3 import app

import subprocess
import json
import re

@app.route('/')
def index():
    return "fartypants"

@app.route('/prefix/<as_set>')
def get_prefix(as_set):
    if not re.match('^AS', as_set):
        abort(403, "Doesn't look like an AS-SET or aut-num - otherwise it would begin 'AS'.  ")
    raw_prefixlist = json.loads(subprocess.check_output(['bgpq3', '-Aj', as_set]))
    return jsonify(raw_prefixlist)