import time
import Adafruit_DHT
from Models.SQLhandler import SQLHandler
from Models.Logging import log
import socket
import requests
from const import UPLOAD_ADRESS


class Dht11(object):

    database = None

    def __init__(self):
        self.database = SQLHandler()

    def read_temp_and_humidity(self):
        hostname = socket.gethostname()
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(11, 17)
            log.info('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
            self.insert_humidity_to_database(humidity, hostname)
            self.insert_temp_to_database(temperature, hostname)
            self.post_data_to_main_server(humidity, temperature, hostname)
            time.sleep(60)

    def insert_temp_to_database(self, temperature, hostname):
        database_entry_temperature = {'sensor_type': 'Temperature',
                                      'sensor_data': temperature,
                                      'sensor_name': '{}RPi_temperature'.format(hostname)}
        self.database.insert('sensor_records', database_entry_temperature)

    def insert_humidity_to_database(self, humidity, hostname):
        database_entry_humidity = {'sensor_type': 'Humidity',
                                   'sensor_data': humidity,
                                   'sensor_name': '{}RPi_humidity'.format(hostname)}
        self.database.insert('sensor_records', database_entry_humidity)

    @staticmethod
    def post_data_to_main_server(humidity, temperature, hostname):
        payload = {'Temperature': temperature, 'Humidity': humidity, 'Hostname': hostname}
        r = requests.post(UPLOAD_ADRESS, data=payload)
        if not r.status_code == requests.codes.ok:
            log.info("Error uploading data")



