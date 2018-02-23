import flask
import numpy as np
import pandas as pd
from copy import deepcopy

# Initialize the app
app = flask.Flask(__name__)

@app.route("/")
def viz_page():
    with open("pair.html", 'r') as viz_file:
        return viz_file.read()

@app.route("/gof", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this url,
    Read the grid from the json, update and send it back
    """
    data = flask.request.json
    a = data['grid']

    # your code for game of life goes here
    # but as first task, just set 'a' to zero
    # and send it back. See if that works.

    return flask.jsonify({'grid': a})

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0', port=5000)