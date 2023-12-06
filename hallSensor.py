class hallSensor:
    def __init__(self, gpioNumber):
        self.pin = gpioNumber
        self.timeSensor = 0
        self.pinState = 1

    def getTimeSensor(self):
        return self.timeSensor

    def getPinState(self):
        return self.pinState

    def getPinNumber(self):
        return self.pin

    def setTimeSensor(self, time):
        self.timeSensor = time

    def setPinState(self, state):
        self.pinState = state