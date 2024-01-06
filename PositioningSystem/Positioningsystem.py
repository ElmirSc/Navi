import sys
sys.path.append("/root")
import RPi.GPIO as GPIO
from speedometer import *
from ownmpu6050 import OwnMpu6050
from positionigSystemConfig import *
from client import Client

gyroAddress = 0x68
hall_pin_forward = 17
hall_pin_backward = 27


class Positioningsystem:
    def __init__(self, hall_pin_forward, hall_pin_backward):
        self.mpu6050 = OwnMpu6050(gyro_range=250)
        self.speedometer = Speedometer(hall_pin_forward, hall_pin_backward)
        self.default_orientation_value = self.mpu6050.get_gyro_z()
        self.default_orientation_value_range = self.default_orientation_value * 0.1
        self.client = Client()

    def get_orientation(self):
        gyro_z_value = self.mpu6050.get_gyro_z()
        if gyro_z_value < (self.default_orientation_value - self.default_orientation_value_range):
            orientation = turn_left
        elif gyro_z_value > (self.default_orientation_value + self.default_orientation_value_range):
            orientation = turn_right
        else:
            orientation = no_turn
        return orientation

    def init_positioning_system(self):
        self.speedometer.init_speedometer()
        self.client.create_socket()

    def get_speed_from_speedometer(self):
        return self.speedometer.get_speed()

    def get_driven_distance_from_speedometer(self):
        return self.speedometer.get_distance()

    def send_speed_distance_rotation_to_server(self):
        speed = self.get_speed_from_speedometer()
        dist = self.get_driven_distance_from_speedometer()
        orientation = self.get_orientation()
        message = (str(speed) + " " + str(dist) + " " + str(orientation))
        self.client.send_message(message)


def start_positioning_system():
    pos_system = Positioningsystem(hall_pin_forward, hall_pin_backward)
    pos_system.init_positioning_system()
    try:
        while True:
            pos_system.speedometer.set_count()
            time.sleep(1)
            pos_system.speedometer.check_direction_tire()
            curren_distance = (pos_system.speedometer.get_count() * ((pos_system.speedometer.get_wheel() * pi) / 4))
            pos_system.speedometer.set_distance(curren_distance)
            pos_system.speedometer.set_speed(curren_distance * 3.6 * pos_system.speedometer.direction)
            pos_system.speedometer.print_stats()
            pos_system.send_speed_distance_rotation_to_server()
    except KeyboardInterrupt:
        pos_system.client.close_connection()
        GPIO.cleanup()


if __name__ == "__main__":
    pos_system = Positioningsystem(hall_pin_forward, hall_pin_backward)
    pos_system.init_positioning_system()
    try:
        while True:
            pos_system.speedometer.set_count()
            time.sleep(1)
            pos_system.speedometer.check_direction_tire()
            currenDistance = (pos_system.speedometer.get_count() * ((pos_system.speedometer.get_wheel() * pi) / 4))
            pos_system.speedometer.set_distance(currenDistance)
            pos_system.speedometer.set_speed(currenDistance * 3.6 * pos_system.speedometer.direction)
            pos_system.speedometer.print_stats()
            pos_system.send_speed_distance_rotation_to_server()
    except KeyboardInterrupt:
        pos_system.client.close_connection()
        GPIO.cleanup()
