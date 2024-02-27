#!/usr/bin/python3
""" Script that starts a Flask web application,
web application listening on 0.0.0.0 and port 5000"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_session(error):
    """Removes the current SQLAlchemy Session after each request"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Helps list all State objects"""
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
