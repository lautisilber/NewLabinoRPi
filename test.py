from gpiozero import DigitalOutputDevice as OutPin
from time import sleep

led = OutPin(17)

state = True
while True:
    led.value = state
    state = not state
    sleep(1)