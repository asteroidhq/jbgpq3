from flask import Flask, request, abort, jsonify
from jbgpq3 import app

import subprocess
import json
import re
import os
import time

CACHE_MAX_AGE_POLICY_SECONDS = 2700 # 45 minutes

@app.route('/')
def index():
    return "fartypants"

@app.route('/prefix/<as_set>')
def get_prefix(as_set):
    if not re.match('^AS', as_set.upper()):
        abort(403, "Doesn't look like an AS-SET or aut-num - otherwise it would begin 'AS'.  ")

    display_prefixlist = {}
    display_prefixlist["as_set"] = as_set

    # Test to see if the cache is too old to use
    if os.path.isfile("/tmp/jbgpq3_4" + as_set):
        filestats = os.stat("/tmp/jbgpq3_4" + as_set)
        file_age = int(time.time() - filestats.st_mtime)

        if file_age > CACHE_MAX_AGE_POLICY_SECONDS:
            # Cache is stale, remove the files and fetch new
            display_prefixlist["cache_deleted"] = True
            os.remove("/tmp/jbgpq3_4" + as_set)
            os.remove("/tmp/jbgpq3_6" + as_set)
            display_prefixlist["cache_hit"] = False
            display_prefixlist["cache_age_seconds"] = 0
        else:
            # Cache is not stale, use the cache
            display_prefixlist["cache_hit"] = True
            display_prefixlist["cache_age_seconds"] = file_age
    else:
        # Cache file does not exist, fetch
        display_prefixlist["cache_hit"] = False
        display_prefixlist["cache_age_seconds"] = 0


    # IPv4 prefixes
    if display_prefixlist["cache_hit"]:
        with open("/tmp/jbgpq3_4" + as_set, "r") as myfile:
            raw_prefixlist = ''.join(myfile.read().splitlines())
    else:
        raw_prefixlist = subprocess.check_output(['bgpq3', '-S', 'RIPE,APNIC,AFRINIC,ARIN,JPIRR,NTTCOM,RADB,ALTDB,BELL,LEVEL3,RGNET,TC', '-A4j', as_set])
        with open("/tmp/jbgpq3_4" + as_set, "w") as myfile:
            myfile.write(raw_prefixlist.decode())
    display_prefixlist["prefixes_ipv4"] = json.loads(raw_prefixlist)["NN"]


    # IPv6 prefixes
    if display_prefixlist["cache_hit"]:
        with open("/tmp/jbgpq3_6" + as_set, "r") as myfile:
            raw_prefixlist = ''.join(myfile.read().splitlines())
    else:
        raw_prefixlist = subprocess.check_output(['bgpq3', '-S', 'RIPE,APNIC,AFRINIC,ARIN,JPIRR,NTTCOM,RADB,ALTDB,BELL,LEVEL3,RGNET,TC', '-A6j', as_set])
        with open("/tmp/jbgpq3_6" + as_set, "w") as myfile:
            myfile.write(raw_prefixlist.decode())
    display_prefixlist["prefixes_ipv6"] = json.loads(raw_prefixlist)["NN"]


    return jsonify(display_prefixlist)
