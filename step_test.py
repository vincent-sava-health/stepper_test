import RPi.GPIO as GPIO
import time

DIR = 24
STEP = 18
EN = 4

STEPS_PER_REV = 200      # 1.8° motor
MICROSTEPS = 32          # change to 16/8/1 if your HAT is set differently
PULSES_PER_REV = STEPS_PER_REV * MICROSTEPS

STEP_DELAY = 0.0005      # 500 us high, 500 us low (~1 kHz). Slow + reliable.

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

# Enable driver (DRV8825: EN low = enabled)
GPIO.output(EN, GPIO.LOW)

def one_revolution(clockwise=True):
    GPIO.output(DIR, GPIO.HIGH if clockwise else GPIO.LOW)
    time.sleep(0.05)  # let DIR settle

    for _ in range(PULSES_PER_REV):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(STEP_DELAY)

try:
    print("1 rev clockwise")
    one_revolution(clockwise=True)
    time.sleep(1)

    print("1 rev counter-clockwise")
    one_revolution(clockwise=False)
    time.sleep(1)

finally:
    # Disable driver and clean up
    GPIO.output(EN, GPIO.HIGH)
    GPIO.cleanup()
