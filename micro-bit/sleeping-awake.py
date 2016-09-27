from microbit import *

while True:

    #display.show(Image.YES)

    if accelerometer.is_gesture('face up'):
        display.show(Image.HAPPY)
    if accelerometer.is_gesture('face down'):
        display.show(Image.ANGRY)

    sleep(1000)
