import RPi.GPIO as GPIO
import time
from hallSensor import hallSensor
import os

pi = 3.141592653

class speedometer:
    def __init__(self, sensorOne, sensorTwo):
        self.hallForward = hallSensor(sensorOne)
        self.hallBack = hallSensor(sensorTwo)
        self.count = 0
        self.speed = 0
        self.direction = 1
        self.distance = 0
        self.wheel = 0.11
        self.initSpeedometer()

    def setDistance(self, newDistance):
        self.distance += newDistance
    def getDistance(self):
        return self.distance
    def getSpeed(self):
        return self.speed

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

        self.hallForward.setPinState(GPIO.input(self.hallForward.getPinNumber()))
        self.hallBack.setPinState(GPIO.input(self.hallBack.getPinNumber()))
        print("Start Werte Vorwaertshall:", self.hallForward.getPinState())
        print("Start Werte Backhall:", self.hallBack.getPinState())
        self.changeEdgeEventSpeedometer(self.hallForward.getPinNumber())
        self.changeEdgeEventSpeedometer(self.hallBack.getPinNumber())

    def changeEdgeEventSpeedometer(self, pin):
        GPIO.remove_event_detect(pin)
        if pin == 17:
            if self.hallForward.pinState == 1:
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=hallSensorCallbackForwardSpeedometer, bouncetime=100)
            else:
                GPIO.add_event_detect(pin, GPIO.RISING, callback=hallSensorCallbackForwardSpeedometer, bouncetime=100)
        elif pin == 27:
            if self.hallBack.pinState == 1:
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=hallSensorCallbackBackSpeedometer, bouncetime=100)
            else:
                GPIO.add_event_detect(pin, GPIO.RISING, callback=hallSensorCallbackBackSpeedometer, bouncetime=100)

    def checkDirectionTire(self):
        if self.hallForward.timeSensor > self.hallBack.timeSensor:
            self.direction = 1
        else:
            self.direction = -1

    def printStats(self):
        print("Current Speed:", self.speed)
        print("Current km:", self.distance)


def hallSensorCallbackForwardSpeedometer(channel):
    global speedometerOne

    #currentPinState = GPIO.input(speedometerOne.hallForward.pin)
    #print("Pinstate:", currentPinState)
    speedometerOne.addToCount()
    speedometerOne.hallForward.timeSensor = time.time()
    speedometerOne.changeEdgeEventSpeedometer(speedometerOne.hallForward.pin)


def hallSensorCallbackBackSpeedometer(channel):
    global speedometerOne

    #currentPinState = GPIO.input(speedometerOne.hallBack.pin)
    #print("Pinstate:", currentPinState)
    speedometerOne.addToCount()
    speedometerOne.hallBack.timeSensor = time.time()
    speedometerOne.changeEdgeEventSpeedometer(speedometerOne.hallBack.pin)

try:
    speedometerOne = speedometer(17, 27)
    while True:
        speedometerOne.setCount()
        time.sleep(1)
        speedometerOne.checkDirectionTire()
        currenDistance = (speedometerOne.getCount() * ((speedometerOne.getWheel() * pi) / 4))
        speedometerOne.setDistance(currenDistance)
        speedometerOne.speed = currenDistance * 3.6 * speedometerOne.direction
        speedometerOne.printStats()



except KeyboardInterrupt:
    GPIO.cleanup()
