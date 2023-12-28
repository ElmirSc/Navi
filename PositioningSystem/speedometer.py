import RPi.GPIO as GPIO
import time
from hallSensor import hallSensor
import os

pi = 3.141592653
speedometerOne = 0

class speedometer:
    def __init__(self, sensorOne, sensorTwo):
        self.hallForward = hallSensor(sensorOne)
        self.hallBack = hallSensor(sensorTwo)
        self.count = 0
        self.speed = 0
        self.direction = 1
        self.distance = 0
        self.wheel = 0.11
        self.pinState = 1
        self.initSpeedometer()
        self.startBool = False


    def setDistance(self, newDistance):
        self.distance += newDistance
    def getDistance(self):
        return self.distance
    def getSpeed(self):
        return self.speed

    def setSpeed(self,curSpeed):
        self.speed = curSpeed

    def getCount(self):
        return self.count

    def setCount(self):
        self.count = 0

    def addToCount(self):
        self.count += 1

    def getWheel(self):
        return self.wheel

    def initSpeedometer(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.hallForward.getPinNumber(), GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.hallBack.getPinNumber(), GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.hallForward.initPinState(GPIO.input(self.hallForward.getPinNumber()))
        self.hallBack.initPinState(GPIO.input(self.hallBack.getPinNumber()))
        self.changeEdgeEventSpeedometer(self.hallForward.getPinNumber())
        self.changeEdgeEventSpeedometer(self.hallBack.getPinNumber())
        self.setDefaultDirection()

    def changeEdgeEventSpeedometer(self, pin):
        GPIO.remove_event_detect(pin)
        if pin == 17:
            if self.hallForward.getPinState() == 1:
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.hallSensorCallbackForwardSpeedometer, bouncetime=100)
            else:
                GPIO.add_event_detect(pin, GPIO.RISING, callback=self.hallSensorCallbackForwardSpeedometer, bouncetime=100)
        elif pin == 27:
            if self.hallBack.getPinState() == 1:
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.hallSensorCallbackBackSpeedometer, bouncetime=100)
            else:
                GPIO.add_event_detect(pin, GPIO.RISING, callback=self.hallSensorCallbackBackSpeedometer, bouncetime=100)

    def checkDirectionTire(self):
        if self.hallForward.timeSensor > self.hallBack.timeSensor:
            self.direction = 1
        else:
            self.direction = -1

    def printStats(self):
        print("Current Speed:", self.speed)
        print("Driven Meters:", self.distance)

    def getStartBool(self):
        return self.startBool

    def setStartBoolToTrue(self):
        self.startBool = True

    def setDefaultDirection(self):
        self.direction = 1


    def hallSensorCallbackForwardSpeedometer(self,channel):
        global speedometerOne
        print("test")
        currentPinState = GPIO.input(speedometerOne.hallForward.pin)
        if speedometerOne.hallForward.getNextPinState() == currentPinState:
            speedometerOne.hallForward.timeSensor = time.time()
            speedometerOne.hallForward.setPinState()
            speedometerOne.changeEdgeEventSpeedometer(speedometerOne.hallForward.pin)
            if speedometerOne.getStartBool():
                speedometerOne.addToCount()
            else:
                speedometerOne.setStartBoolToTrue()


    def hallSensorCallbackBackSpeedometer(self,channel):
        global pos_system
        print("test")
        currentPinState = GPIO.input(speedometerOne.hallBack.pin)
        if speedometerOne.hallBack.getNextPinState() == currentPinState:
            speedometerOne.hallBack.timeSensor = time.time()
            speedometerOne.hallBack.setPinState()
            speedometerOne.changeEdgeEventSpeedometer(speedometerOne.hallBack.pin)


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
