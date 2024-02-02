import sys
import os

sys.path.append("/root")
import RPi.GPIO as GPIO
from speedometer import *
from ownmpu6050 import OwnMpu6050
from positionigSystemConfig import *
from client import Client
from rc_controll import RCModellAuto, control_car
from threading import Thread

gyroAddress = 0x68
hall_pin_forward = 17
hall_pin_backward = 27


# positioning system class for whole system
class Positioningsystem:
    def __init__(self, hall_pin_forward, hall_pin_backward):
        self.mpu6050 = OwnMpu6050(gyro_range=250,filter_range=5)  # mpu6050 object
        self.speedometer = Speedometer(hall_pin_forward, hall_pin_backward)  # speedometer object
        self.default_orientation_value = self.mpu6050.get_gyro_z()  # initial value for rotation of car
        self.default_orientation_value_range = self.default_orientation_value * 0.1  # range of initial state of rotation of car
        self.client = Client()  # client object
        self.orientation_of_car = no_turn
        self.prev_gyro_z_value = 0

    def get_orientation(self):  # function to get orientation of car
        gyro_z_value = self.mpu6050.get_gyro_z()
        print(gyro_z_value)
        if gyro_z_value < -20 and self.orientation_of_car != turn_right and self.prev_gyro_z_value > -20:
            self.orientation_of_car = turn_right
        elif gyro_z_value > 20 and self.orientation_of_car != turn_left and self.prev_gyro_z_value < 20:
            self.orientation_of_car = turn_left
        else:
            self.orientation_of_car = no_turn
        self.prev_gyro_z_value = gyro_z_value


    def init_positioning_system(self):  # function to initialilze positioning system
        self.speedometer.init_speedometer()
        self.mpu6050.init_gyroskop()

    def get_speed_from_speedometer(self):  # function to get speed of speedometer
        return self.speedometer.get_speed()

    def get_driven_distance_from_speedometer(self):  # function to get driven distance of speedometer
        return self.speedometer.get_distance()

    def send_speed_distance_rotation_to_server(self):  # function to send speed, distance and rotation to navigation
        speed = int(self.speedometer.current_speed)
        dist = self.speedometer.current_distance
        print("Speed: ", speed)
        print("Dist: ", dist)
        self.get_orientation()
        if self.orientation_of_car == no_turn:
            print("Keine Drehung")
        elif self.orientation_of_car == turn_right:
            print("Rechtsdrehung")
        elif self.orientation_of_car == turn_left:
            print("Linksdrehung")
        message = (str(speed) + " " + str(dist) + " " + str(self.orientation_of_car))
        self.client.create_socket()
        self.client.send_message(message)

def drive_car_with_keyboard(car):
    try:
        control_car(car)
    finally:
        car.cleanup()

def process_hall_and_mpu6050(pos_system):
    try:
        while True:
            pos_system.speedometer.set_count()
            time.sleep(1)
            curren_distance = (pos_system.speedometer.get_count() * ((pos_system.speedometer.wheel_diameter * pi) / 4))
            pos_system.speedometer.set_distance(curren_distance)
            pos_system.speedometer.set_speed(curren_distance * 3.6 * pos_system.speedometer.direction)
            pos_system.send_speed_distance_rotation_to_server()
    except KeyboardInterrupt:
        pos_system.client.close_connection()
        GPIO.cleanup()

def handle_connection_to_socket(pos_system):
    while True:
        os.system('clear')
        pos_system.send_speed_distance_rotation_to_server()





def start_positioning_system():  # function to start the positioning system
    pos_system = Positioningsystem(hall_pin_forward, hall_pin_backward)
    pos_system.init_positioning_system()
    thread_for_socket_connection = Thread(target=handle_connection_to_socket, args=(pos_system,))
    thread_for_process_all_data = Thread(target=process_hall_and_mpu6050, args=(pos_system,))
    thread_for_socket_connection.start()
    thread_for_process_all_data.start()
    #car = RCModellAuto(motor_pin=13, steering_pin=19)
    try:
        while True:
            pos_system.speedometer.set_count()
            time.sleep(1)
            curren_distance = (pos_system.speedometer.get_count() * ((pos_system.speedometer.get_wheel() * pi) / 4))
            pos_system.speedometer.set_distance(curren_distance)
            pos_system.speedometer.set_speed(curren_distance * 3.6 * pos_system.speedometer.direction)
    except KeyboardInterrupt:
        pos_system.client.close_connection()
        GPIO.cleanup()
        thread_for_socket_connection.join()

    #if pos_system.client.accept_connection():
    #    pos_system.client.receive_message()
    #print(pos_system.client.data)



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
