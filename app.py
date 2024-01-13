from flask import Flask, request
from app_service import AppService
import json
from  db_service import DbService, AirSample
import logging
from datetime import datetime, timedelta
import dateparser
from security import api_required


logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = Flask(__name__)
dbService = DbService()


@app.route('/')
def home():
    return "Hello World!!! version 3.0"


@app.route('/api/sgp40/create', methods=['POST'])
@api_required
def create_sgp40_table():
    dbService.root()
    return "OK"

def to_date(date_string, default): 
    try:
        logger.debug(f"to_date >> {date_string}")
        # return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return dateparser.parse(date_string)
    except ValueError:
        # raise ValueError('{} is not valid date in the format YYYY-MM-DD HH-MM-SS'.format(date_string))
        logger.error(f"{ValueError} in to_date")
        return default


@app.route('/api/sgp40')
def sgp40():
    
    device_id = request.args['device_id'] 
    
    start_time_str = request.args.get('start_time')
    logger.debug(f"start_time_str {start_time_str}")
    start_time = to_date(start_time_str, datetime.now() - timedelta(days=365)) if start_time_str else datetime.now() - timedelta(days=365)
    
    end_time_str = request.args.get('end_time')
    logger.debug(f"end_time_str {end_time_str}")
    end_time = to_date(end_time_str, datetime.now()) if end_time_str else datetime.now()
    logger.debug(f"start_time {start_time}  end_time {end_time}")
    return dbService.get_air_samples(device_id, start_time, end_time)


@app.route('/api/sgp40', methods=['POST'])
@api_required
def create_sgp40():
    request_data = request.get_json()
    sgp40 = request_data['sgp40']
    logging.info(f"create air sampe {sgp40}")
    air_sample = AirSample(**sgp40)
    return dbService.create_air_sample(air_sample)


@app.route('/api/sgp40', methods=['PUT'])
@api_required
def update_sgp40():
    request_data = request.get_json()
    air_sample = AirSample(**request_data['sgp40'])
    return dbService.update_air_sample(air_sample)


@app.route('/api/sgp40/<int:id>', methods=['DELETE'])
@api_required
def delete_sgp40(id):
    return dbService.delete_sgp40(id)

