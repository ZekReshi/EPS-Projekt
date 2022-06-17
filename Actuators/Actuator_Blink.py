import multiprocessing
from Actuators.Actuator import Actuator
from MQTT.vehicledetectionmessage_pb2 import Action
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

blinkThread = None
led_pin = 14
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, False)

def blink_loop():
    on = True
    while True:
        GPIO.output(led_pin, on)
        on = not on
        time.sleep(0.1)

def on_message(action: Action):
    global blinkThread
    if action == Action.ON:
        if blinkThread is None:
            blinkThread = multiprocessing.Process(target=blink_loop, args=())
            blinkThread.start()
    else:
        if blinkThread is not None:
            blinkThread.terminate()
        blinkThread = None
        


def main():
    actuator = Actuator(on_message)
    actuator.on_run()
    if blinkThread is not None:
        blinkThread.terminate()
    GPIO.cleanup() 
    