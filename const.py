import os

BASE = os.path.dirname(os.path.abspath(__file__))
# database path
DB = os.path.join(BASE, 'database', 'weatherinfo.db')
# where to upload data
UPLOAD_ADRESS = 'http://192.168.137.207:8080/weather/receive'
LOG = os.path.join(BASE, 'Logs', 'Log.log')
# upper limit of each data push
DBPUSHLIMIT = 300