class hallSensor:
    def __init__(self, gpioNumber):
        self.pin = gpioNumber
        self.timeSensor = 0
        self.pinState = 1
        self.nextPinState = 1

    def getTimeSensor(self):
        return self.timeSensor

    def getPinState(self):
        return self.pinState

    def getPinNumber(self):
        return self.pin

    def setTimeSensor(self, time):
        self.timeSensor = time

    def setPinState(self):
        if self.pinState == 1:
            self.pinState = 0
            self.nextPinState = 1
        else:
            self.pinState = 1
            self.nextPinState = 0


    def initPinState(self,state):
        self.pinState = state
        if self.pinState == 1:
            self.nextPinState = 0
        else:
            self.nextPinState = 1

    def getNextPinState(self):
        return self.nextPinState