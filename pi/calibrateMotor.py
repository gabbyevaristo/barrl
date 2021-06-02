import RPi.GPIO as GPIO
import time

pinNum = 36
timeSleep = 10 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinNum, GPIO.OUT, initial=GPIO.HIGH)

print("Pin ON")
GPIO.output(pinNum,False)
time.sleep(timeSleep)

GPIO.cleanup()
