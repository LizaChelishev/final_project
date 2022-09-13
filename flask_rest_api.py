from flask import Flask, render_template, jsonify
from flask_cors import CORS
from Business_Logics.AnonymousFacade import AnonymousFacade
from DataAccess.db_repo_pool import db_repo_pool
from templates import *

app = Flask(__name__)
CORS(app)

repool = db_repo_pool.get_instance()


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/flights/tables")
def flights_tables():
    return render_template('flights_tables.html')


@app.route("/flights", methods=['GET'])
def get_all_flights():
    repo = repool.get_connection()  # getting a repo
    anonfcade = AnonymousFacade(repo)
    all_flights = anonfcade.get_all_flights()
    if all_flights:
        flights = [flight.data_for_web() for flight in all_flights]
    else:
        flights = []
    repool.return_connection(repo)  # returning the repo
    return jsonify(flights)


@app.route("/arrivals/<int:hours_num>", methods=['GET'])
def get_arrival_flights_by_delta_t(hours_num):
    repo = repool.get_connection()  # getting a repo
    anonfcade = AnonymousFacade(repo)
    arrivals = anonfcade.get_arrival_flights_by_delta_t(hours_num)
    if arrivals:
        flights = [flight.data_for_web() for flight in arrivals]
    else:
        flights = []
    repool.return_connection(repo)  # returning the repo
    return jsonify(flights)


@app.route("/departures/<int:hours_num>", methods=['GET'])
def get_departure_flights_by_delta_t(hours_num):
    print(type(hours_num))
    repo = repool.get_connection()  # getting a repo
    anonfcade = AnonymousFacade(repo)
    departures = anonfcade.get_departure_flights_by_delta_t(hours_num)
    if departures:
        flights = [flight.data_for_web() for flight in departures]
    else:
        flights = []
    repool.return_connection(repo)  # returning the repo
    return jsonify(flights)


if __name__ == '__main__':
    app.run(debug=True)