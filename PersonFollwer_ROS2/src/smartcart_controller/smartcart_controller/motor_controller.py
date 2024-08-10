import RPi.GPIO as GPIO
# Constants
MAXPWM = 25 

# Define the motor control pins
# A-right B-left
M1PWMA = 12
M1AIN1 = 22
M1AIN2 = 23

M2PWMB = 13
M2BIN1 = 24
M2BIN2 = 25

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1PWMA, GPIO.OUT)
GPIO.setup(M1AIN1, GPIO.OUT)
GPIO.setup(M1AIN2, GPIO.OUT)

GPIO.setup(M2PWMB, GPIO.OUT)
GPIO.setup(M2BIN1, GPIO.OUT)
GPIO.setup(M2BIN2, GPIO.OUT)

# Function to drive motor 1
def drive_motor1(direction):
    GPIO.output(M1AIN1, direction)
    GPIO.output(M1AIN2, not direction)

# Function to drive motor 2
def drive_motor2(direction):
    GPIO.output(M2BIN1, direction)
    GPIO.output(M2BIN2, not direction)

# Main function
def main():
    pwmR = GPIO.PWM(M1PWMA, 10000)
    pwmL = GPIO.PWM(M2PWMB, 10000)
    pwmR.start(75)
    pwmL.start(75)
    try:
        while True:
            print("driving")
            drive_motor1(1)
            # GPIO.output(M1AIN1, 0)
            # GPIO.output(M1AIN2, 1)
            
        
    except KeyboardInterrupt:
        # Stop both motors
        GPIO.output(M1PWMA, GPIO.LOW)
        GPIO.output(M2PWMB, GPIO.LOW)

        # Clean up GPIO
        GPIO.cleanup()

if __name__ == "__main__":
    main()