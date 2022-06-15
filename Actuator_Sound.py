from Actuator import Actuator
from vehicledetectionmessage_pb2 import Action


def on_message(action: Action):
    if action == Action.ON:
        print("ON")
    else:
        print("OFF")


if __name__ == '__main__':
    actuator = Actuator(on_message)
    actuator.on_run()
