mpu6050Address = 0x68  # mpu6050 address on raspberry
smbusPort = 1  # bus port

# scale factor for gyroskop on mpu6050
gyro_scale250_deg = 131.0
gyro_scale500_deg = 65.5
gyro_scale1000_deg = 32.8
gyro_scale2000_deg = 16.4

# range factor for gyroskop on mpu6050
gyro_range250_deg = 0x00
gyro_range500_deg = 0x08
gyro_range1000_deg = 0x10
gyro_range2000_deg = 0x18

# filter values for mpu6050
filter256 = 0x00
filter188 = 0x01
filter98 = 0x02
filter42 = 0x03
filter20 = 0x04
filter10 = 0x05
filter5 = 0x06

pwrmgmt = 0x6B  # register for power managmnet of mpu6050

temperautre_out_reg = 0x41  # register of temparature sensor

gyro_x = 0x43  # address of x of gyroskop
gyro_y = 0x45  # address of y of gyroskop
gyro_z = 0x47  # address of z of gyroskop

gyro_config = 0x1B  # config port for gyroskop on mpu6050
mpu_config = 0x1A  # config port for mpu6050
