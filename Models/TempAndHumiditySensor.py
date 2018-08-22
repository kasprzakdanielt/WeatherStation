import time
import Adafruit_DHT
from Models.SQLhandler import SQLHandler
from Models.Logging import log
import socket
import requests
from const import UPLOAD_ADRESS, DBPUSHLIMIT
import json


class Dht11(object):
    database = None

    def __init__(self):
        self.database = SQLHandler()

    def read_temp_and_humidity(self):
        hostname = socket.gethostname()
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(11, 17)
            log.debug('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
            self.insert_humidity_to_database(humidity, hostname)
            self.insert_temp_to_database(temperature, hostname)
            self.post_data_to_main_server()
            time.sleep(60)

    def insert_temp_to_database(self, temperature, hostname):
        database_entry_temperature = {'sensor_type': 'Temperature',
                                      'sensor_data': temperature,
                                      'sensor_name': hostname}
        self.database.insert('sensor_records', database_entry_temperature)

    def insert_humidity_to_database(self, humidity, hostname):
        database_entry_humidity = {'sensor_type': 'Humidity',
                                   'sensor_data': humidity,
                                   'sensor_name': hostname}
        self.database.insert('sensor_records', database_entry_humidity)

    def post_data_to_main_server(self):
        payload = self.get_data_from_database_to_send(DBPUSHLIMIT)
        attempts = 0
        success = False
        log.debug("Uploading data")
        while attempts < 3 and not success:
            try:
                r = requests.post(UPLOAD_ADRESS, data={'payload': payload})
                if r.status_code == requests.codes.ok:
                    success = True
                    id = r.json()['data']
                    id_decoded = json.loads(id[0])
                    id_list = []
                    for single_id in id_decoded:
                        id_list.append(single_id['sensor_id_child'])
                    self.database.delete('sensor_records', 'sensor_id in {}'.format(tuple(id_list)))
            except requests.exceptions.ConnectionError:
                time.sleep(10)
                attempts += 1
                log.debug("Error uploading data")

    def get_data_from_database_to_send(self, limit):
        payload = self.database.select(
            'select sensor_id, sensor_type, sensor_data, sensor_date, sensor_name from sensor_records LIMIT {}'.format(
                limit))
        return json.dumps(payload)
