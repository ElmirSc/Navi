from mpu6050Config import *
import smbus


# self implemented mpu6050 class
class OwnMpu6050:
    def __init__(self, gyro_range=250, filter_range=20):
        self.mpu6050_address = mpu6050Address  # mpu6050 address
        self.bus = smbus.SMBus(smbusPort)  # creating smbus port
        self.bus.write_byte_data(self.mpu6050_address, pwrmgmt, 0x00)  # wake up MPU-6050
        self.gyroRange = gyro_range  # gyro range for mpu6050
        self.filter_range = filter_range

    def init_mpu6050(self, new_gyro_range, new_filter_range):
        self.filter_range = new_filter_range
        self.gyroRange = new_gyro_range
        self.set_gyro_range()
        self.set_filter_range()

    def read_from_bus(self, register):  # function to read data from bus between raspberry and mpu6050
        # Read data
        high = self.bus.read_byte_data(self.mpu6050_address, register)
        low = self.bus.read_byte_data(self.mpu6050_address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    def get_temperature(self):  # function to get temperature of mpu6050
        raw = self.read_from_bus(temperautre_out_reg)
        temp = (raw / 340.0) + 36.53
        return temp

    def set_gyro_range(self):  # function to set gyroskope range on mpu6050
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.mpu6050_address, gyro_config, 0x00)
        gyro_set_range = 0
        if self.gyroRange == 250:
            gyro_set_range = gyro_range250_deg
        elif self.gyroRange == 500:
            gyro_set_range = gyro_range500_deg
        elif self.gyroRange == 1000:
            gyro_set_range = gyro_range1000_deg
        elif self.gyroRange == 2000:
            gyro_set_range = gyro_range2000_deg

        self.bus.write_byte_data(self.mpu6050_address, gyro_config, gyro_set_range)  # Write new range to register

    def get_gyro_z(self):  # function to get z rotation data from gyroskope
        gyro_z_value = self.read_from_bus(gyro_z)
        gyro_scale = 0

        if self.gyroRange == 250:
            gyro_scale = gyro_scale250_deg
        elif self.gyroRange == 500:
            gyro_scale = gyro_scale500_deg
        elif self.gyroRange == 1000:
            gyro_scale = gyro_scale1000_deg
        elif self.gyroRange == 2000:
            gyro_scale = gyro_scale2000_deg

        gyro_z_value = gyro_z_value / gyro_scale

        return gyro_z_value

    def set_filter_range(self):  # function to set the filter range of mpu6050
        ext = self.bus.read_byte_data(self.mpu6050_address, mpu_config) & 0b00111000  # save current Filter Range
        filter_set_range = 0

        if self.filter_range == 256:
            filter_set_range = filter256
        elif self.filter_range == 188:
            filter_set_range = filter188
        elif self.filter_range == 98:
            filter_set_range = filter98
        elif self.filter_range == 42:
            filter_set_range = filter42
        elif self.filter_range == 20:
            filter_set_range = filter20
        elif self.filter_range == 10:
            filter_set_range = filter10
        elif self.filter_range == 5:
            filter_set_range = filter5
        else:
            print("Parameter has wrong Filter Range!")

        return self.bus.write_byte_data(self.mpu6050_address, mpu_config, ext | filter_set_range)

    def init_gyroskop(self):
        self.set_gyro_range()
        self.set_filter_range()


if __name__ == "__main__":
    mpu6050 = OwnMpu6050()
    mpu6050.init_mpu6050(250, 20)
    try:
        print(mpu6050.get_gyro_z())
    except KeyboardInterrupt:
        print("Finish")

