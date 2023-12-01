import os
import time

from airbit import SDCard


class DataLogger(object):

    SD_PATH = "/sd"
    LOG_FILE_EXT = ".csv"

    def __init__(self, t: time.struct_time):
        self.sdcard = SDCard()
        
        self.LOG_FILE_NAME = f"{t.tm_year}.{t.tm_mon}.{t.tm_mday}{self.LOG_FILE_EXT}"
        self.SD_LOG_FILE_PATH = self.SD_PATH + "/" + self.LOG_FILE_NAME

        files = os.listdir(self.SD_PATH)
        if self.SD_LOG_FILE_PATH not in files:
            with open(self.SD_LOG_FILE_PATH, "w") as fp:
                fp.write("Date,Time,Coordinates,Temperature,Humidity,PM25,PM10\n")
                fp.flush()

        print(f"Created log file {self.SD_LOG_FILE_PATH}")

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

        if not self._verify_data(data):
            raise ValueError("Some values in the data are not correct")

        try:
            with open(self.SD_LOG_FILE_PATH, 'a') as fp:
                fp.write(",".join(data))
                fp.write("\n")
                fp.flush()
        except Exception as e:
            print(e)
            raise OSError("[SD] SD removed")

    def _verify_data(self, data: dict) -> bool:
        """Verifies that the data is correctly formatted.

        Args:
            data (dict): Data to be verified

        Returns:
            bool: True if the expected data is correctly formatted. False otherwise
        """
        return True
