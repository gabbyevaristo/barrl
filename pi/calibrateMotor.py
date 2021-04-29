import RPi.GPIO as GPIO
import time

pinNum = 36
timeSleep = 60 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinNum, GPIO.OUT, initial=GPIO.HIGH)
# # loop through 3 times, on for 5 seconds/off for 1 second
# for i in range(3):
#     print("Pin ON")
#     GPIO.output(pinNum,False)
#     time.sleep(5)
#     GPIO.output(pinNum,True)
#     print("Pin Off")
#     time.sleep(1)

print("Pin ON")
GPIO.output(pinNum,False)
time.sleep(timeSleep)


GPIO.cleanup()
