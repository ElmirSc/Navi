import RPi.GPIO as GPIO
import time
import keyboard

class RCModellAuto:
    def __init__(self, motor_pin, steering_pin):
        self.motor_pin = motor_pin
        self.steering_pin = steering_pin
        self.pwm_frequency = 50
        self.pwm_motor = None
        self.pwm_servo = None
        self.setup()

    def setup(self):
        # Initialisiert die GPIO-Pins
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.steering_pin, GPIO.OUT)
        self.pwm_servo = GPIO.PWM(self.steering_pin, self.pwm_frequency)
        self.pwm_motor = GPIO.PWM(self.motor_pin, self.pwm_frequency)
        print("Fahrzeug einschalten!")
        self.pwm_servo.start(7.0)
        time.sleep(1)
        self.pwm_motor.start(6.0)
        time.sleep(10)

    def drive(self, speed):
        # Bewegt das Auto vorwerts
        self.pwm_motor.ChangeDutyCycle(speed)

    def steer(self, angle):
        # Steuert die Richtung
        self.pwm_servo.ChangeDutyCycle(angle)

    def stop(self):
        # Haelt das Auto an
        self.pwm_servo.stop()
        self.pwm_motor.stop()

    def cleanup(self):
        # Bereinigt die GPIO-Pins
        GPIO.cleanup()

def control_car(car):
    while True:
        if keyboard.is_pressed('w'):  # Vorwärts fahren, wenn W gedrückt wird
            car.drive(7.5)
        elif keyboard.is_pressed('s'):  # Rückwärts fahren, wenn S gedrückt wird
            car.drive(4.0)
        elif keyboard.is_pressed('a'):  # Nach links steuern, wenn A gedrückt wird
            car.steer(5.0)
        elif keyboard.is_pressed('d'):  # Nach rechts steuern, wenn D gedrückt wird
            car.steer(10.0)
        elif keyboard.is_pressed('x'):  # Stoppen, wenn X gedrückt wird
            car.stop()
            break
        time.sleep(0.1)  # Kurze Pause, um das Polling zu begrenzen

# Beispiel zur Verwendung der Klasse
if __name__ == "__main__":
    car = RCModellAuto(motor_pin=13, steering_pin=19)

    try:
        control_car(car)
    finally:
        car.cleanup()
