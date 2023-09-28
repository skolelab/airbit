
import time
import busio

from adafruit_gps import GPS



class UltimateGPS:
    def __init__(self, tx, rx):

        self.uart = busio.UART(tx, rx, baudrate=9600, timeout=30)
        self.GPS = GPS(uart=self.uart, debug=False)
    
        self.previous_update = None

    def update(self):

        if not self.GPS.update():
            return False
        
        if not self.GPS.has_fix:
            print("[GPS] Waiting for fix")
            return False
        
        self.previous_update = (self.GPS.latitude, self.GPS.longitude, self.GPS.timestamp_utc)

        return True


    def get_coordinates(self):

        if not self.update() and self.previous_update is not None:
            return self.previous_update[0], self.previous_update[1]
        
        return self.GPS.latitude, self.GPS.longitude
    
    def get_time(self):
        
        if not self.update() and self.previous_update is not None:
            return self.previous_update[2]
        
        return self.GPS.timestamp_utc