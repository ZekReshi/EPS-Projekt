from Actuators.Actuator import Actuator
from MQTT.vehicledetectionmessage_pb2 import Action


def on_message(action: Action):
    if action == Action.ON:
        print("ON")
    else:
        print("OFF")


def main():
    actuator = Actuator(on_message)
    actuator.on_run()
