#!/usr/bin/python3
"""
Creates app_views of a flask app
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """"
    create a route /status on the object app_views
    that returns a JSON: "status": "OK"
    """

    response = ('status': "OK")
    return jsonify(response)
