import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_socketio import SocketIO
from config import ServiceConfig
from redis_listener import RedisListener
from influxdb_controller import InfluxDBController
from socketio_controller import SocketIOController

config = ServiceConfig()
app = Flask(__name__, template_folder='templates', static_folder='static')
influxdb_controller = InfluxDBController(
    host=config.influxdb_host,
    database=config.influxdb_db,
    username=config.influxdb_admin_user,
    password=config.influxdb_admin_password
)
socketio_controller = SocketIOController(emitter=SocketIO(app=app, async_mode='eventlet'))
redis_listener = RedisListener(
    redis_host=config.redis_host,
    redis_channel=config.channel_name,
    actions=[influxdb_controller.write_tickers_data, socketio_controller.emit_data]
)
redis_listener.start()


@app.route('/')
def index():
    """
    Home page
    """
    return render_template('index.html')


@app.route('/ticker_names')
def get_ticker_names():
    """
    API endpoint to get a list of available instruments
    """
    return jsonify(influxdb_controller.get_tickers_list())


@app.route('/ticker_data')
def get_ticker_data():
    """
    API endpoint to get stored prices data for
    an instrument specified via query string
    parameter "ticker_name"
    """
    ticker_name = request.args.get('ticker_name')
    points = influxdb_controller.get_ticker_data(ticker_name=ticker_name)
    data = [
        [datetime.datetime.fromisoformat(point['time'].replace('Z', '')).timestamp(), point['price']]
        for point in points
    ]
    return jsonify(data)


@app.route('/favicon.ico')
def favicon():
    """
    Returns favicon
    """
    return send_from_directory(
        directory='./static',
        path='images/favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

