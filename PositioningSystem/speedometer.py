import RPi.GPIO as GPIO
import time
from hallSensor import hallSensor

pi = 3.141592653
speedometerOne = 0


class Speedometer:
    def __init__(self, sensor_one, sensor_two):
        self.hall_forward_sensor = hallSensor(sensor_one)
        self.hall_back_sensor = hallSensor(sensor_two)
        self.counter_for_speed_and_dist = 0
        self.current_speed = 0
        self.direction = 1
        self.current_distance = 0
        self.wheel_diameter = 0.11
        self.pin_state = 1
        self.init_speedometer()
        self.start_bool = False

    def set_distance(self, new_distance):
        self.current_distance += new_distance

    def get_distance(self):
        return self.current_distance

    def get_speed(self):
        return self.current_speed

    def set_speed(self, cur_speed):
        self.current_speed = cur_speed

    def get_count(self):
        return self.counter_for_speed_and_dist

    def set_count(self):
        self.counter_for_speed_and_dist = 0

    def add_to_count(self):
        self.counter_for_speed_and_dist += 1

    def get_wheel(self):
        return self.wheel_diameter

    def init_speedometer(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.hall_forward_sensor.get_pin_number(), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.hall_back_sensor.get_pin_number(), GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.hall_forward_sensor.init_pin_state(GPIO.input(self.hall_forward_sensor.get_pin_number()))
        self.hall_back_sensor.init_pin_state(GPIO.input(self.hall_back_sensor.get_pin_number()))
        self.change_edge_event_speedometer(self.hall_forward_sensor.get_pin_number())
        self.change_edge_event_speedometer(self.hall_back_sensor.get_pin_number())
        self.set_default_direction()

    def change_edge_event_speedometer(self, pin):
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
                GPIO.add_event_detect(pin, GPIO.RISING, callback=self.hall_sensor_callback_back_speedometer, bouncetime=100)

    def check_direction_tire(self):
        if self.hall_forward_sensor.time_sensor > self.hall_back_sensor.time_sensor:
            self.direction = 1
        else:
            self.direction = -1

    def print_stats(self):
        print("Current Speed:", self.current_speed)
        print("Driven Meters:", self.current_distance)

    def get_start_bool(self):
        return self.start_bool

    def set_start_bool_to_true(self):
        self.start_bool = True

    def set_default_direction(self):
        self.direction = 1

    def hall_sensor_callback_forward_speedometer(self, channel):
        current_pin_state = GPIO.input(self.hall_forward_sensor.pin)
        if self.hall_forward_sensor.get_next_pin_state() == current_pin_state:
            self.hall_forward_sensor.time_sensor = time.time()
            self.hall_forward_sensor.set_pin_state()
            self.change_edge_event_speedometer(self.hall_forward_sensor.pin)
            if self.get_start_bool():
                self.add_to_count()
            else:
                self.set_start_bool_to_true()

    def hall_sensor_callback_back_speedometer(self, channel):
        current_pin_state = GPIO.input(self.hall_back_sensor.pin)
        if self.hall_back_sensor.get_next_pin_state() == current_pin_state:
            self.hall_back_sensor.time_sensor = time.time()
            self.hall_back_sensor.set_pin_state()
            self.change_edge_event_speedometer(self.hall_back_sensor.pin)

# try:
#     speedometerOne = speedometer(17, 27)
#     while True:
#         speedometerOne.setCount()
#         time.sleep(1)
#         #speedometerOne.checkDirectionTire()
#         currenDistance = (speedometerOne.getCount() * ((speedometerOne.getWheel() * pi) / 4))
#         speedometerOne.setDistance(currenDistance)
#         speedometerOne.setSpeed(currenDistance * 3.6 * speedometerOne.direction)
#         speedometerOne.printStats()
#
#
#
# except KeyboardInterrupt:
#     GPIO.cleanup()
