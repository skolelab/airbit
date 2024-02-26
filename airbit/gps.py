
import busio
import board
import rtc
import time

from adafruit_gps import GPS



class UltimateGPS:
    def __init__(self, tx=board.GP16, rx=board.GP17) -> None:

        self.uart = busio.UART(tx, rx, baudrate=9600, timeout=30)
        self.GPS = GPS(uart=self.uart, debug=False)

        self.clock = None
        self.clock_sync = False
        self.previous_update = None
    
    def _update(self) -> bool:

        if not self.GPS.update():
            return False
        
        if not self.GPS.has_fix:
            print("[GPS] Waiting for fix")
            return False
        
        self.previous_update = (self.GPS.latitude, self.GPS.longitude, self.GPS.timestamp_utc)

        return True

    def sync_clock(self) -> bool:
        """Try to sync the Real Time Clock, using the GPS timestamp.

        Returns:
            bool: True if the clock was synched, False otherwise.
        """

        if self._update() and self.GPS.timestamp_utc.tm_year == 2023:

            r = rtc.RTC()
            r.datetime = self.GPS.timestamp_utc
            self.clock_sync = True

            return True
        
        return False

    def get_coordinates(self) -> tuple[float, float]:
        """Get the current coordinates of the GPS.

        Returns:
            tuple[float, float]: Tuple containing (lat, lon) coordinates as floats.

            The position will be the previous if the GPS could not update, or None
            if no previous position is available.
        """

        if not self._update() and self.previous_update is not None:
            return self.previous_update[0], self.previous_update[1]
        
        return self.GPS.latitude, self.GPS.longitude
    
    def get_time(self) -> time.struct_time:
        return rtc.datetime