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
        payload = [{'Temperature': temperature, 'Humidity': humidity, 'Hostname': hostname, 'Date':'' },
                   {'Temperature': temperature, 'Humidity': humidity, 'Hostname': hostname, 'Date': ''}
                   {'Temperature': temperature, 'Humidity': humidity, 'Hostname': hostname, 'Date': ''}]
        attempts = 0
        success = False
        log.info("Uploading data {}".format(hostname))
        while attempts < 3 and not success:
            try:
                r = requests.post(UPLOAD_ADRESS, data=payload)
                if r.status_code == requests.codes.ok:
                    success = True
            except requests.exceptions.ConnectionError:
                time.sleep(10)
                attempts += 1
                log.info("Error uploading data")

    def get_data_from_database_to_send(self, limit):
        lista = self.database.select('select sensor_id, sensor_type, sensor_data, sensor_date, sensor_name from sensor_records LIMIT {}'.format(limit))
        lista_do_wyslania = []
        id_list = []
        for x in lista:
            lista_do_wyslania.append({'sensor_type':x[1], 'sensor_data': x[2], 'sensord_date': x[3], 'sensor_name': x[4]})
            id_list.append({'sensor_id': x[0]})
        return lista_do_wyslania, id_list

