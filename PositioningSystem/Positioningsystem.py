import sys

sys.path.append("/root")
sys.path.append("/home/pi/Desktop/Navi")
import RPi.GPIO as GPIO
from speedometer import *
from ownmpu6050 import OwnMpu6050
from positionigSystemConfig import *
from client import Client
from server import Server
from rc_controll import RCModellAuto, control_car
from threading import Thread

gyroAddress = 0x68
hall_pin_forward = 17
hall_pin_backward = 27
motor_pin = 13
steering_pin = 19


# positioning system class for whole system
class Positioningsystem:
    def __init__(self):
        self.mpu6050 = OwnMpu6050(gyro_range=250, filter_range=5)  # mpu6050 object
        self.speedometer = Speedometer(hall_pin_forward, hall_pin_backward)  # speedometer object
        self.default_orientation_value = self.mpu6050.get_gyro_z()  # initial value for rotation of car
        self.default_orientation_value_range = self.default_orientation_value * 0.1  # range of initial state of rotation of car
        self.server_line_detection = Server("192.168.0.103", 5557)  # client object
        self.client_gui = Client("192.168.0.101", 5556)
        self.orientation_of_car = no_turn
        self.prev_turn = 0
        self.in_turn = False
        self.counted_turn = True
        self.test_var = {"links": 0, "rechts": 0}
        self.route = None
        self.rc_control_car = RCModellAuto(motor_pin=motor_pin, steering_pin=steering_pin)
        self.thread_one = None

    def get_orientation(self):
        gyro_z_value = self.mpu6050.get_gyro_z()
        print("Gyro Z: ", gyro_z_value)

        if gyro_z_value < -turn_threshold and not self.in_turn:
            self.in_turn = True
            self.orientation_of_car = turn_right
            self.counted_turn = False
        elif gyro_z_value > turn_threshold and not self.in_turn:
            self.in_turn = True
            self.orientation_of_car = turn_left
            self.counted_turn = False
        elif -no_turn_threshold < gyro_z_value < no_turn_threshold and self.in_turn:
            self.in_turn = False
            self.orientation_of_car = no_turn

    def init_positioning_system(self):  # function to initialilze positioning system
        print("Initializing system")
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
        if self.orientation_of_car == turn_left and not self.counted_turn:
            self.counted_turn = True
            self.test_var["links"] += 1
            print("Links")
        elif self.orientation_of_car == turn_right and not self.counted_turn:
            self.counted_turn = True
            self.test_var["rechts"] += 1
            print("Rechts")
        elif self.orientation_of_car == no_turn:
            print("Keine drehung")
        print(self.test_var)
        message = (str(speed) + " " + str(dist) + " " + str(self.orientation_of_car))
        self.orientation_of_car = no_turn
        self.client_gui.send_message(message)

    def handle_connection_to_server_line_detection(self):
        print("Hello")
        self.server_line_detection.create_socket()
        self.server_line_detection.set_socket_to_listen_mode()
        self.server_line_detection.accept_connection()
        while True:
            self.server_line_detection.receive_data()
            print(self.server_line_detection.data)


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
            # pos_system.send_speed_distance_rotation_to_server()
    except KeyboardInterrupt:
        pos_system.client.close_connection()
        GPIO.cleanup()


def handle_connection_to_socket(pos_system):
    while True:
        os.system('clear')
        pos_system.send_speed_distance_rotation_to_server()


def start_positioning_system():  # function to start the positioning system
    pos_system = Positioningsystem()
    pos_system.init_positioning_system()
    pos_system.client_gui.connect_to_socket()
    pos_system.thread_one = Thread(target=pos_system.handle_connection_to_server_line_detection())
    try:
        pos_system.client_gui.receive_message()
        print(pos_system.client_gui.data)
        while True:
            pos_system.speedometer.set_count()
            time.sleep(1)
            os.system('clear')
            curren_distance = (pos_system.speedometer.get_count() * ((pos_system.speedometer.wheel_diameter * pi) / 4))
            pos_system.speedometer.set_distance(curren_distance)
            pos_system.speedometer.set_speed(curren_distance * 3.6 * pos_system.speedometer.direction)
            pos_system.send_speed_distance_rotation_to_server()
            pos_system.client_gui.receive_message()
            if pos_system.client_gui.data != None:
                print("Received Data: ", pos_system.client_gui.data)
                if pos_system.client_gui.data == 0:
                    pos_system.speedometer.current_distance = 0
                pos_system.client_gui.data = None
    except KeyboardInterrupt:
        pos_system.client_gui.close_connection()
        GPIO.cleanup()


def test_rotation_of_car(pos_system):
    test_var = {"links": 0, "rechts": 0}
    try:
        while True:
            os.system('clear')
            pos_system.get_orientation()
            if pos_system.orientation_of_car == turn_left and not pos_system.counted_turn:
                test_var["links"] += 1
                pos_system.counted_turn = True
                print("Links")
            elif pos_system.orientation_of_car == turn_right and not pos_system.counted_turn:
                test_var["rechts"] += 1
                pos_system.counted_turn = True
                print("Rechts")
            elif pos_system.orientation_of_car == no_turn:
                print("Keine drehung")
            print(test_var)
    except KeyboardInterrupt:
        print("Finished")


if __name__ == "__main__":
    pos_system = Positioningsystem(hall_pin_forward, hall_pin_backward)
    pos_system.init_positioning_system()
    test_rotation_of_car(pos_system)
    # try:
    #     while True:
    #         pos_system.speedometer.set_count()
    #         time.sleep(1)
    #         pos_system.speedometer.check_direction_tire()
    #         currenDistance = (pos_system.speedometer.get_count() * ((pos_system.speedometer.get_wheel() * pi) / 4))
    #         pos_system.speedometer.set_distance(currenDistance)
    #         pos_system.speedometer.set_speed(currenDistance * 3.6 * pos_system.speedometer.direction)
    #         pos_system.speedometer.print_stats()
    #         pos_system.send_speed_distance_rotation_to_server()
    # except KeyboardInterrupt:
    #     pos_system.client.close_connection()
    #     GPIO.cleanup()
