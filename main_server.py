
from flask import Flask, render_template, jsonify, request, make_response
import uuid
import json
from flask_cors import CORS


from Business_Logics.AirlineFacade import AirlineFacade
from Business_Logics.AdministratorFacade import AdministratorFacade
from Business_Logics.CustomerFacade import CustomerFacade
from ApplicationLogger import *
from DataBaseGenerator import RabbitProducer
from DataBaseGenerator.RabbitConsumer import RabbitConsumerObject
from DataBaseGenerator.RabbitProducer import RabbitProducerObject
from threadLockManager import ThreadLockManager

config = ConfigParser()
config.read('config.conf')

logger = Logger.get_instance()
rabbit_producer = RabbitProducerObject('db_requests')
lock_manager = ThreadLockManager.get_instance()

app = Flask(__name__)

app.register_blueprint(CustomerFacade, url_prefix="/customer")
app.register_blueprint(AirlineFacade, url_prefix="/airline")
app.register_blueprint(AdministratorFacade, url_prefix="/admin")

app.config['SECRET_KEY']: str = config['server']['jwt_secret_key']  # for the jwt encoding

CORS(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    pass


@app.route('/signup', methods=['POST'])  # add customer
def signup():
    global lock_manager
    request_id: str = str(uuid.uuid4())

    new_data: dict = request.get_json()
    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'post', 'resource': 'customer', 'data': new_data}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    if answer_from_core['error'] == 'NotValidDataError':
        return make_response(jsonify(answer_from_core), 409)
    elif answer_from_core['error'] is None:
        return make_response(jsonify(answer_from_core), 200)


@app.route('/flights')  # get all flights, get flights by params, by airline
def flights():
    global lock_manager
    request_id: str = str(uuid.uuid4())

    # query params
    airline_id = request.args.get('airline_id')
    origin_country_id = request.args.get('origin_country_id')
    destination_country_id = request.args.get('destination_country_id')
    date = request.args.get('date')

    if airline_id:
        try:
            airline_id = int(airline_id)
        except ValueError:
            pass
        rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'flight',
                                            'filter': 'airline_id',
                                            'airline_id': airline_id}))
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        if answer_from_core['error'] == 'NotValidDataError':
            return make_response(jsonify(answer_from_core), 400)
        elif answer_from_core['error'] is None:
            return make_response(jsonify(answer_from_core), 200)

    if origin_country_id and destination_country_id and date:
        try:
            origin_country_id_int = int(origin_country_id)
            destination_country_id_int = int(destination_country_id)
            rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'flight',
                                                'filter': 'params',
                                                'origin_country_id': origin_country_id_int,
                                                'destination_country_id': destination_country_id_int, 'date': date}))
            lock_manager.lock_thread(request_id)
            answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
            if answer_from_core['error'] == 'NotValidDataError':
                return make_response(jsonify(answer_from_core), 400)
            elif answer_from_core['error'] is None:
                return make_response(jsonify(answer_from_core), 200)
        except ValueError:
            pass
        rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'flight',
                                            'filter': 'params',
                                            'origin_country_id': origin_country_id,
                                            'destination_country_id': destination_country_id, 'date': date}))
        lock_manager.lock_thread(request_id)
        answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
        if answer_from_core['error'] == 'NotValidDataError':
            return make_response(jsonify(answer_from_core), 400)
        elif answer_from_core['error'] is None:
            return make_response(jsonify(answer_from_core), 200)

    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'flight'}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    return make_response(jsonify(answer_from_core), 200)


@app.route("/flights/tables")
def flights_tables():
    return render_template('flights_tables.html')


@app.route('/flights/arrivals/<int:delta_t>')  # get arrivals by delta t
def arrival_flights(delta_t):
    global lock_manager
    request_id: str = str(uuid.uuid4())

    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'flight',
                                        'filter': 'arrivals_delta_t',
                                        'arrivals_delta_t': delta_t}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    if answer_from_core['error'] == 'NotValidDataError':
        return make_response(jsonify(answer_from_core), 400)
    elif answer_from_core['error'] is None:
        return make_response(jsonify(answer_from_core), 200)


@app.route('/flights/departures/<int:delta_t>')  # get departures by delta t
def departure_flights(delta_t):
    global lock_manager
    request_id: str = str(uuid.uuid4())

    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'flight',
                                        'filter': 'departures_delta_t',
                                        'departures_delta_t': delta_t}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    if answer_from_core['error'] == 'NotValidDataError':
        return make_response(jsonify(answer_from_core), 400)
    elif answer_from_core['error'] is None:
        return make_response(jsonify(answer_from_core), 200)


@app.route('/flights/<int:id_>')  # get flight by id
def flight_by_id(id_):
    global lock_manager
    request_id: str = str(uuid.uuid4())

    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'flight', 'resource_id': id_}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    if answer_from_core['error'] == 'NotValidDataError':
        return make_response(jsonify(answer_from_core), 400)
    elif answer_from_core['error'] is None:
        return make_response(jsonify(answer_from_core), 200)


@app.route('/airlines')  # get all airlines
def airlines():
    global lock_manager
    request_id: str = str(uuid.uuid4())

    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'airline'}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    return make_response(jsonify(answer_from_core), 200)


@app.route('/airlines/<int:id_>')  # get airline by id
def airline_by_id(id_):
    global lock_manager
    request_id: str = str(uuid.uuid4())

    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'airline', 'resource_id': id_}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    if answer_from_core['error'] == 'NotValidDataError':
        return make_response(jsonify(answer_from_core), 400)
    elif answer_from_core['error'] is None:
        return make_response(jsonify(answer_from_core), 200)


@app.route('/countries')  # get all countries
def countries():
    global lock_manager
    request_id: str = str(uuid.uuid4())
    print(request_id)

    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'country'}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    return make_response(jsonify(answer_from_core), 200)


@app.route('/countries/<int:id_>')  # get country by id
def country_by_id(id_):
    global lock_manager
    request_id: str = str(uuid.uuid4())

    rabbit_producer.publish(json.dumps({'id_': request_id, 'method': 'get', 'resource': 'country', 'resource_id': id_}))
    lock_manager.lock_thread(request_id)
    answer_from_core: dict = lock_manager.get_answer(request_id=request_id)
    if answer_from_core['error'] == 'NotValidDataError':
        return make_response(jsonify(answer_from_core), 400)
    elif answer_from_core['error'] is None:
        return make_response(jsonify(answer_from_core), 200)


if __name__ == '__main__':
    app.run()

