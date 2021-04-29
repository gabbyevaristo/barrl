try:
    import RPi.GPIO as GPIO
except:
    pass
    
import time

def pour_water():
    print("Pouring Water")
    pinNum = 36
    timeSleep = 180
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pinNum, GPIO.OUT, initial=GPIO.HIGH)

    print("Pin ON")
    GPIO.output(pinNum,False)
    time.sleep(timeSleep)
    GPIO.cleanup()
