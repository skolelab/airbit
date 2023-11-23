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

    def log(self, data):

        if self.sdcard is None:
            print("[SD] Unable to write to SDCard")
            raise OSError("SDcard not available")
        
        self.log_sd(data)
        


    def log_sd(self, data):

        if not self.verify_data(data):
            raise ValueError("Some values in the data are not correct")

        try:
            with open(self.SD_LOG_FILE_PATH, 'a') as fp:
                fp.write(",".join(data))
                fp.write("\n")
                fp.flush()
        except Exception as e:
            print(e)
            raise OSError("[SD] SD removed")

    def verify_data(self, data):
        return True
