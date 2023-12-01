
import sys
import time
import busio
import board

import adafruit_pm25.uart


class DustSensor:
    def __init__(self, tx=board.GP8, rx=board.GP9) -> None:

        self.uart = busio.UART(tx, rx, baudrate=9600, timeout=30)
        self.pm25 = adafruit_pm25.uart.PM25_UART(self.uart, None)

    def get_airquality(self) -> dict:
        """Get the current measurement of air quality.

        The sensor measures PM1.0, PM2.5 and PM10.0 concentration.
        As well as particulate matter in bins of: 0.3, 0.5, 1.0, 2.5, 5.0, 10.0

        Returns:
            dict: Dict containing the different measurements.

            If the measurement cannot be performed, the method returns None.
        """
        try:
            data = self.pm25.read()

        except RuntimeError as r:
            return None
        
        return data