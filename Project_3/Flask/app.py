import flask
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix

#---------- MODEL IN MEMORY ----------------#

# Read the scientific data on breast cancer survival,
# Build a LogisticRegression predictor on it
with open("yhat.pkl", 'rb') as picklefile: 
    yhat = pickle.load(picklefile)
    
with open("ccdf_upsampled_test.pkl", 'rb') as picklefile: 
    ccdf_up = pickle.load(picklefile)

y_up_test = ccdf_up.default    


def cost(cm, ca_rate):
    tn, fp, fn, tp = cm.ravel()
    cost = (tn) + (tp * ca_rate) + (fp * ca_rate) #- (fn * ca_rate)
    return cost


def get_costlist(yhat, ca_rate):
    cost_list = []
    for i in yhat:
        cm=confusion_matrix(y_up_test, i, labels=None)
        cost_list.append(cost(cm, ca_rate))
    return cost_list

def get_score(cost_list, tn, fp, fn, tp, ca_rate):
    
    return max(cost_list)/(tn + fp + (fn + tp)*ca_rate)

#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__)

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("awesome.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return it's score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = data["example"]
    print(x[0])
    cost_list = get_costlist(yhat, x[0]) 
    
    index = 0
    for i in cost_list:
        if max(cost_list) == i:
            ind = index
            index = index + 1
        else:
            index = index + 1
    tn, fp, fn, tp = confusion_matrix(y_up_test, yhat[ind], labels=None).ravel()
    score = get_score(cost_list, tn, fp, fn, tp, x[0])
    print(score)
    # Put the result in a nice dict so we can send it as json
    results = {"score": score, "tn": float(tn), "fp": float(fp), "fn": float(fn), "tp": float(tp)}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0')
app.run(debug=True)