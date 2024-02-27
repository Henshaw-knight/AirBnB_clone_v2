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


@app.route("/cities_by_states", strict_slashes=False)
def state_cities():
    """Displays cities of each state"""
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
