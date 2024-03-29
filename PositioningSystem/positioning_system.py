import sys
import threading

sys.path.append("/root")
sys.path.append("/home/pi/Desktop/Navi")
import RPi.GPIO as GPIO
from speedometer import *
from mpu6050_own import OwnMpu6050
from positioning_system_config import *
from client import Client
from threading import Thread
import time

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
        # self.server_line_detection = Server("10.27.100.25", 5557)  # client object
        self.client_gui = Client("172.20.10.5", 5556)
        self.orientation_of_car = no_turn
        self.prev_turn = 0
        self.in_turn = False
        self.counted_turn = True
        self.test_var = {"links": 0, "rechts": 0}
        self.route = None
        self.thread = None
        self.thread_lock = threading.Lock()
        self.gyro_val = 0
        self.start_time_of_measuring_gyroskop = 0
        self.end_time_of_measuring_gyroskop = 0
        self.integrated_gyro_val = 0

    def get_orientation(self):
        self.gyro_val = self.mpu6050.get_gyro_z()
        print("Gyro Z: ", self.gyro_val)

        if self.gyro_val < -turn_threshold_implementation_one and not self.in_turn:
            self.in_turn = True
            self.orientation_of_car = turn_right
            self.counted_turn = False
        elif self.gyro_val > turn_threshold_implementation_one and not self.in_turn:
            self.in_turn = True
            self.orientation_of_car = turn_left
            self.counted_turn = False
        elif -no_turn_threshold < self.gyro_val < no_turn_threshold and self.in_turn:
            self.in_turn = False
            self.orientation_of_car = no_turn

    def get_orientation_two(self):
        self.gyro_val = self.mpu6050.get_gyro_z()

        self.end_time_of_measuring_gyroskop = time.time()
        time_diff = self.end_time_of_measuring_gyroskop - self.start_time_of_measuring_gyroskop

        print("Gyro Z: ", self.gyro_val)

        gyro_val_in_degree = self.gyro_val / time_diff
        print("Gyro_Val in Grad: ", gyro_val_in_degree)

        self.start_time_of_measuring_gyroskop = self.end_time_of_measuring_gyroskop

        if -no_turn_threshold > self.gyro_val or no_turn_threshold < self.gyro_val:
            self.integrated_gyro_val += gyro_val_in_degree
        print("Complete Degree:", self.integrated_gyro_val)

        if self.integrated_gyro_val < -turn_threshold_implementation_two and not self.in_turn:
            self.in_turn = True
            self.orientation_of_car = turn_right
            self.counted_turn = False
        elif self.integrated_gyro_val > turn_threshold_implementation_two and not self.in_turn:
            self.in_turn = True
            self.orientation_of_car = turn_left
            self.counted_turn = False
        elif -no_turn_threshold < self.gyro_val < no_turn_threshold and self.in_turn:
            self.in_turn = False
            self.orientation_of_car = no_turn
            self.integrated_gyro_val = 0.0

    def init_positioning_system(self):  # function to initialilze positioning system
        print("Initializing system")
        self.speedometer.init_speedometer()
        self.mpu6050.init_gyroskop()

    def send_speed_distance_rotation_to_server(self):  # function to send speed, distance and rotation to navigation
        self.start_time_of_measuring_gyroskop = time.time()
        while True:
            self.thread_lock.acquire()
            try:
                speed = int(self.speedometer.current_speed)
                dist = self.speedometer.current_distance
            finally:
                self.thread_lock.release()
            print("Speed: ", speed)
            print("Dist: ", dist)
            self.get_orientation_two()
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
            message = str(speed) + " " + str(dist) + " " + str(self.orientation_of_car)
            self.orientation_of_car = no_turn
            print(message)
            self.client_gui.send_message(message)
            time.sleep(0.6)

    def calc_speed(self):
        while True:
            self.speedometer.set_count()
            time.sleep(1)
            os.system('clear')
            self.speedometer.check_direction_tire()
            self.thread_lock.acquire()
            try:
                curren_distance = (self.speedometer.get_count() * ((self.speedometer.wheel_diameter * pi) / 4))
                self.speedometer.set_speed(curren_distance * 3.6 * self.speedometer.direction)
            finally:
                self.thread_lock.release()


def start_positioning_system():  # function to start the positioning system
    print("starting positioning system")
    pos_system = Positioningsystem()
    pos_system.init_positioning_system()
    if not pos_system.client_gui.is_connected:
        print("trying connection to Serversocket")
        pos_system.client_gui.connect_to_socket()
    pos_system.client_gui.receive_message()
    print(pos_system.client_gui.data)

    pos_system.client_gui.connected_client.settimeout(0.01)
    try:
        pos_system.thread = Thread(target=pos_system.send_speed_distance_rotation_to_server)
        pos_system.thread.start()
        pos_system.calc_speed()

    except KeyboardInterrupt:
        pos_system.client_gui.close_connection()
        pos_system.thread.join()
        GPIO.cleanup()


if __name__ == "__main__":
    pos_system = Positioningsystem()
    pos_system.init_positioning_system()
