from Navigation.Navigation import navigation
import RPi.GPIO as GPIO
import sys

sys.path.append('/Navigation/Navigation.py')

if __name__ == "__main__":
    navigation = navigation()
    try:
        while True:
            print("Geschwindigkeit des Fahrzeugs: ",navigation.positioningSystem.speedometer.getSpeed(),"km/h")
            print("Gefahrene Distanz: ", navigation.positioningSystem.speedometer.getDistance(),"m")

    except KeyboardInterrupt:
        GPIO.cleanup()
