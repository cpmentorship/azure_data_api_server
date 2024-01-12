from flask import Flask, request
from app_service import AppService
import json
from  db_service import DbService, AirSample
import logging


app = Flask(__name__)
dbService = DbService()


@app.route('/')
def home():
    return "Hello World!!! version 2.1"

@app.route('/api/sgp40/create', methods=['POST'])
def create_sgp40_table():
    dbService.root()
    return "OK"

@app.route('/api/sgp40')
def sgp40():
    device_id = request.args['device_id'] 
    return dbService.get_air_samples(device_id)

@app.route('/api/sgp40', methods=['POST'])
def create_sgp40():
    request_data = request.get_json()
    sgp40 = request_data['sgp40']
    logging.info(f"create air sampe {sgp40}")
    air_sample = AirSample(**sgp40)
    return dbService.create_air_sample(air_sample)


@app.route('/api/sgp40', methods=['PUT'])
def update_sgp40():
    request_data = request.get_json()
    air_sample = AirSample(**request_data['sgp40'])
    return dbService.update_air_sample(air_sample)


@app.route('/api/sgp40/<int:id>', methods=['DELETE'])
def delete_sgp40(id):
    return dbService.delete_sgp40(id)

