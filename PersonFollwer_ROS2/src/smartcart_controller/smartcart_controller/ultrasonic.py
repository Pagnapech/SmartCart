import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIGF = 5 #29 pin on board
ECHOF = 6 #31 pin oin board

TRIGB = 16 #35 pin on board
ECHOB = 26 #37 pin oin board


print("Distance Measurement in Progress")

GPIO.setup(TRIGF,GPIO.OUT)
GPIO.setup(ECHOF,GPIO.IN)
print("Wating for sensor")
time.sleep(2)

GPIO.output(TRIGF, True)
time.sleep(0.00001)
GPIO.output(TRIGF, False)

while GPIO.input(ECHOF) ==0:
    pulse_start = time.time()


while GPIO.input(ECHOF) ==1:
    pulse_end = time.time()
    
pulse_duration = pulse_end - pulse_start
#distance in cm
distance = pulse_duration * 17150
distance = round(distance, 2)
#distance2 in feet
distance2 = round(distance / 30.48, 2)

print("Distance:",distance,"cm")
print("Distance:",distance2,"feet")
GPIO.cleanup()
