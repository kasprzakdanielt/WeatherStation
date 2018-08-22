from Models.Logging import log
from Models import TempAndHumiditySensor

if __name__ == '__main__':
    log.info("Temperature and humidity started")
    TAH = TempAndHumiditySensor.Dht11()
    TAH.read_temp_and_humidity()
