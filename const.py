import os

BASE = os.path.join(os.getcwd())
DB = os.path.join(BASE, 'database', 'weatherinfo.db')
UPLOAD_ADRESS = 'http://192.168.137.207:8080/weather/receive'
LOG = os.path.join(BASE, 'Logs', 'Log.log')
