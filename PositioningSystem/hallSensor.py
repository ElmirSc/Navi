class hallSensor:
    def __init__(self, gpioNumber):
        self.pin = gpioNumber
        self.time_sensor = 0
        self.pin_state = 1
        self.next_pin_state = 1

    def get_time_sensor(self):
        return self.time_sensor

    def get_pin_state(self):
        return self.pin_state

    def get_pin_number(self):
        return self.pin

    def set_time_sensor(self, time):
        self.time_sensor = time

    def set_pin_state(self):
        if self.pin_state == 1:
            self.pin_state = 0
            self.next_pin_state = 1
        else:
            self.pin_state = 1
            self.next_pin_state = 0

    def init_pin_state(self, state):
        self.pin_state = state
        if self.pin_state == 1:
            self.next_pin_state = 0
        else:
            self.next_pin_state = 1

    def get_next_pin_state(self):
        return self.next_pin_state
