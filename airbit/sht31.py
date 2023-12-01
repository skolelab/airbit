

import board
import busio
from adafruit_sht31d import SHT31D



class SHT31(SHT31D):
    def __init__(self, sda=board.GP14, scl=board.GP15) -> None:
        self.sda = sda
        self.scl = scl

        try:
            self.i2c = busio.I2C(self.scl, self.sda)
        except RuntimeError as e:
            print(e)
            print(f"Temp/Hum sensor does not seem to be connected to pin 14 & 15")
            return None

        super(SHT31, self).__init__(self.i2c)



    def get_temp_hum(self) -> tuple[float, float]:
        """Get the current temperature and humidity.

        Returns:
            tuple[float, float]: The current temperature (in C) and relative humidity (in %)
        """
        return self.temperature, self.relative_humidity
    
