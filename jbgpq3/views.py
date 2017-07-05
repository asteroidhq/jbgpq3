from flask import Flask, request, abort, jsonify
from jbgpq3 import app

@app.route('/')
def index():
    return "fartypants"