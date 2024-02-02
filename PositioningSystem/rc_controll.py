import RPi.GPIO as GPIO
import time

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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.steering_pin, GPIO.OUT)
        self.pwm_servo = GPIO.PWM(self.steering_pin, self.pwm_frequency)
        self.pwm_motor = GPIO.PWM(self.motor_pin, self.pwm_frequency)
        self.pwm_servo.start(7.0)
        sleep(1)
        self.pwm_motor.start(6.0)
        sleep(10)

    def forward(self, speed):
        # Bewegt das Auto vorwerts
        self.pwm_motor.ChangeDutyCycle(speed)

    def reverse(self, speed):
        # Bewegt das Auto rueckwerts
        return 0

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

# Beispiel zur Verwendung der Klasse
if __name__ == "__main__":
    car = RCModellAuto(motor_pin=13, steering_pin=19)

    try:
        car.forward(5)  # Geschwindigkeit anpassen
        car.steer(5)    # Lenkwinkel anpassen
        time.sleep(5)
        car.stop()
    finally:
        car.cleanup()
