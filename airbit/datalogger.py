import os
import time

from airbit import SDCard


class DataLogger(object):

    SD_PATH = "/sd"
    LOG_FILE_EXT = ".csv"

    def __init__(self, t: time.struct_time):
        self.sdcard = SDCard()
        
        self.LOG_FILE_NAME = f"{t.tm_year:02d}-{t.tm_mon:02d}-{t.tm_mday:02d}{self.LOG_FILE_EXT}"
        self.SD_LOG_FILE_PATH = self.SD_PATH + "/" + self.LOG_FILE_NAME

        files = os.listdir(self.SD_PATH)

        if self.LOG_FILE_NAME not in files:
            with open(self.SD_LOG_FILE_PATH, "w") as fp:
                fp.write("Date(DD.MM.YYYY),Time(HH:MM:SS),Lat,Lon,Temperature(°C),Humidity(%),PM25,PM100\n")
                fp.flush()
            print(f"Created log file {self.SD_LOG_FILE_PATH}")

        else:
            print(f"Using existing log file: {self.SD_LOG_FILE_PATH}")

    def log(self, data: dict) -> None:
        """Checks if an SD card is present and calls the log_sd method.

        Args:
            data (dict): The data to be logged.

        Raises:
            OSError: Raised if an SD card object has not been created.
        """

        if self.sdcard is None:
            print("[SD] Unable to write to SDCard")
            raise OSError("SDcard not available")
        
        self.log_sd(data)
        
    def log_sd(self, data: dict) -> None:
        """Calls verify data and logs the data to the SD card.

        Args:
            data (dict): The data to be logged.

        Raises:
            ValueError: Raised if the data is malformed, or missing components.
            OSError: Raised if the SD card is not accessible. (If it has been removed.)
        """

        try:
            data = self._verify_data(data)

        except KeyError:
            print("Missing or malformed data")
            raise

        try:
            with open(self.SD_LOG_FILE_PATH, 'a') as fp:
                fp.write(",".join(data))
                fp.write("\n")
                fp.flush()
        except Exception as e:
            print(e)
            raise OSError("[SD] SD removed")

    def _verify_data(self, data: dict) -> (bool, list):
        """Verifies that the data is correctly formatted.

        Args:
            data (dict): Data to be verified

        Returns:
            list: List containing data converted to strings.
        """
        formatted_data = []

        dt = data["datetime"]
        coords = data["coordinates"]
        temphum = data["temphum"]
        dust = data["dust"]

        if dt is None:
            dt = time.struct_time()

        if coords is None:
            coords = (None, None)
        
        if temphum is None:
            temphum = (None, None)

        if dust is None:
            dust = {"pm25 standard": None, "pm100 standard": None}

                
        formatted_data.append(f"{dt.tm_mday:02d}.{dt.tm_mon:02d}.{dt.tm_year:04d}")
        formatted_data.append(f"{dt.tm_hour:02d}:{dt.tm_min:02d}:{dt.tm_sec:02d}")
        formatted_data.append(f"{coords[0]},{coords[1]}")
        formatted_data.append(f"{temphum[0]:.1f}")
        formatted_data.append(f"{temphum[1]:.1f}")
        formatted_data.append(f"{dust['pm25 standard']:.1f}")
        formatted_data.append(f"{dust['pm100 standard']:.1f}")


        return formatted_data
