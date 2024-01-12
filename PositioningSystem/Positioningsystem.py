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


# positioning system class for whole system
class Positioningsystem:
    def __init__(self, hall_pin_forward, hall_pin_backward):
        self.mpu6050 = OwnMpu6050(gyro_range=250)  # mpu6050 object
        self.speedometer = Speedometer(hall_pin_forward, hall_pin_backward)  # speedometer object
        self.default_orientation_value = self.mpu6050.get_gyro_z()  # initial value for rotation of car
        self.default_orientation_value_range = self.default_orientation_value * 0.1  # range of initial state of rotation of car
        self.client = Client()  # client object

    def get_orientation(self):  # function to get orientation of car
        gyro_z_value = self.mpu6050.get_gyro_z()
        if gyro_z_value < (self.default_orientation_value - self.default_orientation_value_range):
            orientation = turn_left
        elif gyro_z_value > (self.default_orientation_value + self.default_orientation_value_range):
            orientation = turn_right
        else:
            orientation = no_turn
        return orientation

    def init_positioning_system(self):  # function to initialilze positioning system
        self.speedometer.init_speedometer()
        self.client.create_socket()

    def get_speed_from_speedometer(self):  # function to get speed of speedometer
        return self.speedometer.get_speed()

    def get_driven_distance_from_speedometer(self):  # function to get driven distance of speedometer
        return self.speedometer.get_distance()

    def send_speed_distance_rotation_to_server(self):  # function to send speed, distance and rotation to navigation
        speed = int(self.speedometer.current_speed)
        dist = self.speedometer.current_distance
        print("Speed: ", speed)
        print("Dist: ", dist)
        orientation = self.get_orientation()
        if orientation == 0:
            print("Keine Drehung")
        elif orientation == 1:
            print("Rechtsdrehung")
        elif orientation == 2:
            print("Linksdrehung")
        message = (str(speed) + " " + str(dist) + " " + str(orientation))
        self.client.create_socket()
        self.client.send_message(message)


def start_positioning_system():  # function to start the positioning system
    pos_system = Positioningsystem(hall_pin_forward, hall_pin_backward)
    pos_system.init_positioning_system()
    try:
        while True:
            pos_system.speedometer.set_count()
            time.sleep(1)
            #pos_system.speedometer.check_direction_tire()
            curren_distance = (pos_system.speedometer.get_count() * ((pos_system.speedometer.get_wheel() * pi) / 4))
            pos_system.speedometer.set_distance(curren_distance)
            pos_system.speedometer.set_speed(curren_distance * 3.6 * pos_system.speedometer.direction)
            #pos_system.speedometer.print_stats()
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
