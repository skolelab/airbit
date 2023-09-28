
import sys
import time
import busio


import adafruit_pm25.uart




class DustSensor:
    def __init__(self, tx, rx):

        self.uart = busio.UART(tx, rx, baudrate=9600, timeout=30)
        self.pm25 = adafruit_pm25.uart.PM25_UART(self.uart, None)

    def get_airquality(self):
        try:
            data = self.pm25.read()

        except RuntimeError as r:
            return None
        
        return data