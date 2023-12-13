from mpu6050Config import *
import time
import smbus

class mpu6050:
    def __init__(self, gyroRange = 250):
        self.mpu6050Adress = mpu6050Address
        self.bus = smbus.SMBus(smbusPort)
        self.bus.write_byte_data(self.mpu6050Adress,PWRMGMT, 0x00) # Wake up MPU-6050
        self.gyroRange = gyroRange

    def readFromBus(self, register):
        # Read data
        high = self.bus.read_byte_data(self.mpu6050Adress, register)
        low = self.bus.read_byte_data(self.mpu6050Adress, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    def getTemperature(self):
        raw = self.readFromBus(TemperautreOutReg)
        temp = (raw / 340.0) + 36.53
        return temp

    def setGyroRange(self, gyroRange):
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.mpu6050Adress, GyroConfig, 0x00)
        gyroSetRange = 0
        match gyroRange:
            case 250:
                gyroSetRange = GyroRange250DEG
            case 500:
                gyroSetRange = GyroRange500DEG
            case 1000:
                gyroSetRange = GyroRange1000DEG
            case 2000:
                gyroSetRange = GyroRange2000DEG

        self.bus.write_byte_data(self.mpu6050Adress, GyroConfig, gyroSetRange) # Write new range to register

    def getGyroZ(self):
        gyroZ = self.readFromBus(GyroZ)
        gyroScale = 0

        match self.gyroRange:
            case 250:
                gyroScale = GyroScale250DEG
            case 500:
                gyroScale = GyroScale500DEG
            case 1000:
                gyroScale = GyroScale1000DEG
            case 2000:
                gyroScale = GyroScale2000DEG


        gyroZ = gyroZ / gyroScale

        return gyroZ

    def setFilterRange(self, filterRange):
        EXT = self.bus.read_byte_data(self.mpu6050Adress, MPUConfig) & 0b00111000 # save current Filter Range
        filterSetRange = 0
        match filterRange:
            case 256:
                filterSetRange = Filter256
            case 188:
                filterSetRange = Filter188
            case 98:
                filterSetRange = Filter98
            case 42:
                filterSetRange = Filter42
            case 20:
                filterSetRange = Filter20
            case 10:
                filterSetRange = Filter10
            case 5:
                filterSetRange = Filter5
            case _:
                print("Parameter has wrong Filter Range!")

        return self.bus.write_byte_data(self.mpu6050Adress, MPUConfig,  EXT | filterSetRange)
