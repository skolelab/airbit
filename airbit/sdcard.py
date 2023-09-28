
import board
import busio
import sdcardio
import storage

class SDCard:
    def __init__(self, cs=board.GP5, sck=board.GP2, mosi=board.GP3, miso=board.GP4):
        self.spi = busio.SPI(sck, MOSI=mosi, MISO=miso)

        try:
            self.SD = sdcardio.SDCard(self.spi, cs=cs)

        except OSError as e:
            print("[SD] SD card not found or removed")
            raise
    
        self.vfs = storage.VfsFat(self.SD)

        storage.mount(self.vfs, "/sd")