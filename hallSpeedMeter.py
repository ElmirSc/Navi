import os

import RPi.GPIO as GPIO
import time
from hallSensor import hallSensor

hallSensorForward = 17
hallSensorBack = 27
pi = 3.1415
wheel = 0.11
speed = 0
direction = 1
fullDistance = 0
count = 0
timeSensorForward = 0
timeSensorBack = 0
forwardPinState = 1
backPinState = 1


def hallSensorCallbackForward(channel):
    global count
    global timeSensorForward
    global forwardPinState
    global hallSensorForward

    currentPinState = GPIO.input(hallSensorForward)
    #print("Pinstate:", currentPinState)
    count += 1
    timeSensorForward = time.time()
    changeEdgeEvent(hallSensorForward, currentPinState)


def hallSensorCallbackBack(channel):
    global count
    global timeSensorBack
    global backPinState
    global hallSensorBack

    currentPinState = GPIO.input(hallSensorBack)
    #print("Pinstate:", currentPinState)
    count += 1
    timeSensorBack = time.time()
    changeEdgeEvent(hallSensorBack, currentPinState)


def checkDirection():
    global timeSensorBack
    global timeSensorForward
    global direction

    if timeSensorBack < timeSensorForward:
        direction = -1
    else:
        direction = 1


def init():
    global forwardPinState
    global backPinState
    global hallSensorForward
    global hallSensorBack

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(hallSensorForward, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(hallSensorBack, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    forwardPinState = GPIO.input(hallSensorForward)
    backPinState = GPIO.input(hallSensorBack)
    print("Start Werte Vorwaertshall:", forwardPinState)
    print("Start Werte Backhall:", backPinState)
    changeEdgeEvent(hallSensorForward, forwardPinState)
    changeEdgeEvent(hallSensorBack, backPinState)


def changeEdgeEvent(pin, state):
    GPIO.remove_event_detect(pin)
    if pin == 17:
        if state == 1:
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=hallSensorCallbackForward, bouncetime=100)
        else:
            GPIO.add_event_detect(pin, GPIO.RISING, callback=hallSensorCallbackForward, bouncetime=100)
    elif pin == 27:
        if state == 1:
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=hallSensorCallbackBack, bouncetime=100)
        else:
            GPIO.add_event_detect(pin, GPIO.RISING, callback=hallSensorCallbackBack, bouncetime=100)


try:
    init()
    while True:
        count = 0
        time.sleep(1)
        #print("Zeit F:", timeSensorForward)
        #print("Zeit B:", timeSensorBack)
        checkDirection()
        currenDistance = (count * ((wheel * pi) / 4))
        fullDistance = fullDistance + currenDistance
        speed = currenDistance * 3.6 * direction
        print("Zurckgelegte Strecke:", fullDistance)
        print("Geschwindigkeit:", speed)
        os.system('clear')


except KeyboardInterrupt:
    GPIO.cleanup()
