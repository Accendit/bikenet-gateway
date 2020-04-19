import serial
from time import sleep
import struct

class Bike:
    def __init__(self, ser: serial.Serial):
        self.ser = ser

    def getStatus(self):
        self.ser.write(b'\x01')
        response = self.ser.read_until(b'\x0A')
        return self.__read__(response)

    def unlock(self):
        self.ser.write(b'\x02')

    def __read__(self, data):
        return {
            "bike": data[2],
            "latitude": struct.unpack('f', data[4:8])[0],
            "longitude": struct.unpack('f', data[9:13])[0],
            "unlockable": struct.unpack('?', data[14:15])[0],
            "locked": struct.unpack('?', data[16:17])[0]
        }


if __name__ == '__main__':
    ser = serial.Serial(port='COM3', baudrate=9600, timeout=2)
    sleep(2)
    bike = Bike(ser)
    print(bike.getStatus())
    ser.close()