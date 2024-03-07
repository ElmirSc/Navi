import RPi.GPIO as GPIO
import time
from hallsensor import Hallsensor
import os

pi = 3.141592653
speedometerOne = 0


# speedometer class to get data from hallsensors
class Speedometer:
    def __init__(self, sensor_one, sensor_two):
        self.hall_forward_sensor = Hallsensor(sensor_one)  # object of forward hall sensor
        self.hall_back_sensor = Hallsensor(sensor_two)  # object of back hall sensor
        self.counter_for_speed_and_dist = 0  # counter for speed and distance
        self.current_speed = 0
        self.direction = 1
        self.current_distance = 0
        self.wheel_diameter = 0.114
        self.pin_state = 1
        self.start_bool = False

    def set_distance(self, new_distance):  # function to set the distance
        self.current_distance += new_distance

    def set_speed(self, cur_speed):  # function to set speed value
        self.current_speed = int(cur_speed)

    def get_count(self):  # function to get counter value
        return self.counter_for_speed_and_dist

    def set_count(self):  # function to set counter value to zero
        self.counter_for_speed_and_dist = 0

    def add_to_count(self):  # function to add 1 to counter
        self.counter_for_speed_and_dist += 1

    def get_wheel(self):  # function to get wheel diameter value to calc dist and speed
        return self.wheel_diameter

    def init_speedometer(self):  # function to initialize speedometer
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.hall_forward_sensor.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.hall_back_sensor.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.hall_forward_sensor.init_pin_state(GPIO.input(self.hall_forward_sensor.pin))
        self.hall_back_sensor.init_pin_state(GPIO.input(self.hall_back_sensor.pin))
        self.change_edge_event_speedometer(self.hall_forward_sensor.pin)
        self.change_edge_event_speedometer(self.hall_back_sensor.pin)
        self.set_default_direction()

    def change_edge_event_speedometer(self, pin):  # function to change the edge event of pins
        GPIO.remove_event_detect(pin)
        if pin == 17:
            if self.hall_forward_sensor.get_pin_state() == 1:
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.hall_sensor_callback_forward_speedometer,
                                      bouncetime=100)
            else:
                GPIO.add_event_detect(pin, GPIO.RISING, callback=self.hall_sensor_callback_forward_speedometer,
                                      bouncetime=100)
        elif pin == 27:
            if self.hall_back_sensor.get_pin_state() == 1:
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.hall_sensor_callback_back_speedometer,
                                      bouncetime=100)
            else:
                GPIO.add_event_detect(pin, GPIO.RISING, callback=self.hall_sensor_callback_back_speedometer,
                                      bouncetime=100)

    def check_direction_tire(self):  # function to check driving direction
        if self.hall_forward_sensor.time_sensor > self.hall_back_sensor.time_sensor:
            self.direction = 1
        else:
            self.direction = -1

    def print_stats(self):  # function to print stats of speedometer
        print("Current Speed:", self.current_speed)
        print("Driven Meters:", self.current_distance)

    def get_start_bool(self):  # function to get bool value to add 1 to counter value
        return self.start_bool

    def set_start_bool_to_true(self):  # function to set the start bool to True
        self.start_bool = True

    def set_default_direction(self):  # function to set default tire direction
        self.direction = 1

    def hall_sensor_callback_forward_speedometer(self,
                                                 channel):  # callback funtion to add 1 to counter if falling or rising edge is detectet for forward hallsensor
        current_pin_state = GPIO.input(self.hall_forward_sensor.pin)
        if self.hall_forward_sensor.get_next_pin_state() == current_pin_state:
            self.hall_forward_sensor.time_sensor = time.time()
            self.hall_forward_sensor.set_pin_state()
            self.change_edge_event_speedometer(self.hall_forward_sensor.pin)
            if self.get_start_bool():
                self.add_to_count()
            else:
                self.set_start_bool_to_true()

    def hall_sensor_callback_back_speedometer(self,
                                              channel):  # callback funtion to add 1 to counter if falling or rising edge is detectet for back hallsensor
        current_pin_state = GPIO.input(self.hall_back_sensor.pin)
        if self.hall_back_sensor.get_next_pin_state() == current_pin_state:
            self.hall_back_sensor.time_sensor = time.time()
            self.hall_back_sensor.set_pin_state()
            self.change_edge_event_speedometer(self.hall_back_sensor.pin)

if __name__ == '__main__':
    speedometer = Speedometer(17,27)
    speedometer.init_speedometer()
    try:
        while True:
            speedometer.set_count()
            time.sleep(1)
            os.system('clear')
            curren_distance = (speedometer.get_count() * ((speedometer.wheel_diameter * pi) / 4))
            speedometer.set_distance(curren_distance)
            speedometer.set_speed(curren_distance * 3.6 * speedometer.direction)
            speedometer.print_stats()
    except KeyboardInterrupt:
        GPIO.cleanup()

