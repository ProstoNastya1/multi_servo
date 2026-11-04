import pigpio
import time

SERVO1 = 17
SERVO2 = 18

MIN_PULSE = 1000
MAX_PULSE = 2000
CENTER_PULSE = 1500

pi = pigpio.pi()

if not pi.connected:
    print("Cannot connect to pigpio daemon.")
    print("Run: sudo pigpiod")
    exit()

pi.set_mode(SERVO1, pigpio.OUTPUT)
pi.set_mode(SERVO2, pigpio.OUTPUT)


def set_angle(pin, angle):
    angle = max(0, min(180, angle))

    pulse = MIN_PULSE + (
        (MAX_PULSE - MIN_PULSE) * angle / 180
    )

    pi.set_servo_pulsewidth(pin, pulse)


try:
    # Center both servos
    print("Center")
    set_angle(SERVO1, 90)
    set_angle(SERVO2, 90)
    time.sleep(2)

    # Servo 1 only
    print("Servo 1")
    set_angle(SERVO1, 0)
    time.sleep(1)

    set_angle(SERVO1, 180)
    time.sleep(1)

    set_angle(SERVO1, 90)
    time.sleep(1)

    # Servo 2 only
    print("Servo 2")
    set_angle(SERVO2, 0)
    time.sleep(1)

    set_angle(SERVO2, 180)
    time.sleep(1)

    set_angle(SERVO2, 90)
    time.sleep(1)

    # Both servos simultaneously
    print("Both servos")

    while True:

        for angle in range(0, 181, 3):

            set_angle(SERVO1, angle)
            set_angle(SERVO2, 180 - angle)

            time.sleep(0.03)

        for angle in range(180, -1, -3):

            set_angle(SERVO1, angle)
            set_angle(SERVO2, 180 - angle)

            time.sleep(0.03)


except KeyboardInterrupt:
    print("\nStopping...")


finally:
    pi.set_servo_pulsewidth(SERVO1, 0)
    pi.set_servo_pulsewidth(SERVO2, 0)

    pi.stop()
