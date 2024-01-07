# class to create the hallsensor objects
class Hallsensor:
    def __init__(self, gpioNumber):
        self.pin = gpioNumber  # hallsensor pin
        self.time_sensor = 0  # time from pin
        self.pin_state = 1  # current hallsensor state
        self.next_pin_state = 1  # next hallsensor state

    def get_time_sensor(self):  # function to get time from sensor
        return self.time_sensor

    def get_pin_state(self):  # function to get pin state of hallsensor
        return self.pin_state

    def get_pin_number(self):  # function to get the pin of the hallsensor
        return self.pin

    def set_time_sensor(self, time):  # function to set time of sensor
        self.time_sensor = time

    def set_pin_state(self):  # function to set the next state of hallsensor
        if self.pin_state == 1:
            self.pin_state = 0
            self.next_pin_state = 1
        else:
            self.pin_state = 1
            self.next_pin_state = 0

    def init_pin_state(self, state):  # init function for hallsensor
        self.pin_state = state
        if self.pin_state == 1:
            self.next_pin_state = 0
        else:
            self.next_pin_state = 1

    def get_next_pin_state(self):  # function to get next pinstate
        return self.next_pin_state
