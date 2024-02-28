#!/usr/bin/python3
""" Script that starts a Flask web application,
web application listening on 0.0.0.0 and port 5000"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def end_session(err):
    """Removes the current SQLAlchemy Session after each request"""
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """Displays list of all State objects"""
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)


@app.route("/states/<id>", strict_slashes=False)
def state_by_id(id=None):
    """Displays State object found by id"""
    state = None
    states = storage.all(State).values()
    for spec_state in states:
        if spec_state.id == id:
            state = spec_state
    return render_template('9-states.html', state=state)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
