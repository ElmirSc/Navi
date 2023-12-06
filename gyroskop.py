from mpu6050 import mpu6050

sensor = mpu6050(0x68)

try:
    while True:
        print("Gyroskop X:", sensor.GYRO_XOUT0)
        print("Gyroskop Y:", sensor.GYRO_YOUT0)
        print("Gyroskop Z:", sensor.GYRO_ZOUT0)

except KeyboardInterrupt:
    print("exceeded")

class gyro:
    def __init__(self,address):
        self.gyroskopAdress = address
        self.sensor = mpu6050(address)
        self.GyroX = 0
        self.GyroY = 0
        self.GyroZ = 0

    def getGyroAxes(self):
        return self.sensor.GYRO_XOUT0 , self.sensor.GYRO_YOUT0, self.sensor.GYRO_YOUT0

    def getGyroX(self):
        self.GyroX = self.sensor.GYRO_XOUT0
        return self.GyroX

    def getGyroY(self):
        self.GyroY = self.sensor.GYRO_YOUT0
        return self.GyroY

    def getGyroZ(self):
        self.GyroZ = self.sensor.GYRO_ZOUT0
        return self.GyroZ