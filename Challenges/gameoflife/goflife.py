import flask
import numpy as np
import pandas as pd
from copy import deepcopy

# Initialize the app
app = flask.Flask(__name__)


def update_node(neighbor_sum, node):
    if node == 1:
        if neighbor_sum == 0:
            return 0
        elif neighbor_sum > 3:
            return 0 
        else:
            return 1
    else:
        if neighbor_sum == 3:
            return 1
        else:
            return 0
        
def update(grid):
    M, N = grid.shape
    new_grid = grid.copy()
    for i in range(1,M-1):
        for j in range(1,N-1):
            neighbor_sum = grid[i-1:i+2,j-1:j+2].sum() - grid[i,j]
            new_grid[i,j] = update_node(neighbor_sum, grid[i,j])
    return new_grid

def play_game(grid):
    #for step in range(steps):
       # print(step)
    new_grid = update(grid)
        #display.clear_output(wait=True)
        #plt.imshow(new_grid, cmap='gray', interpolation='nearest')
        
        #plt.show()
        #time.sleep(.1)
    grid = new_grid
    return grid


@app.route("/")
def viz_page():
    with open("index.html", 'r') as viz_file:
        return viz_file.read()

@app.route("/gof", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this url,
    Read the grid from the json, update and send it back
    """
    data = flask.request.json
    a = data['grid']
    print(a)
    
    b = list(np.zeros(len(a)))

    # your code for game of life goes here
    # but as first task, just set 'a' to zero
    # and send it back. See if that works.

    return flask.jsonify({'grid': b})

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0', port=5000)