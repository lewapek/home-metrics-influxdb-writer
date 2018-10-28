import logging
import sys

from flask import Flask
from flask import request
from influxdb import InfluxDBClient

from src import settings
from src.influx_utils import influx_points

app = Flask("collector")
app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
app.logger.setLevel(logging.INFO)

client = InfluxDBClient(settings.influx.host, settings.influx.port, settings.influx.user, settings.influx.password,
                        settings.influx.database)
client.create_database(settings.influx.database)

app.logger.info("Successfully connected to influxdb")


@app.route('/measure', methods=['POST'])
def measure():
    json_body = request.get_json()
    app.logger.info("Got request: %s", json_body)
    all_points = influx_points(json_body)
    client.write_points(all_points)
    return "accepted", 202


app.run(host=settings.collector.host, port=settings.collector.port)
