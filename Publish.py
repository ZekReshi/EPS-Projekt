import paho.mqtt.client as mqtt

import vehicledetectionmessage_pb2
from vehicledetectionmessage_pb2 import Action


class Publisher:
    mqtt_client: mqtt.Client
    proto_msg: vehicledetectionmessage_pb2.PBMessage

    def __init__(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("iot.soft.uni-linz.ac.at", 1883, 60)
        self.proto_msg = vehicledetectionmessage_pb2.PBMessage()

    def send_on(self):
        self.proto_msg.control.action = Action.ON
        self.mqtt_client.publish("camera/emergency-light", self.proto_msg.SerializeToString())

    def send_off(self):
        self.proto_msg.control.action = Action.OFF
        self.mqtt_client.publish("camera/emergency-light", self.proto_msg.SerializeToString())

    def send(self, on):
        if on:
            self.send_on()
        else:
            self.send_off()

