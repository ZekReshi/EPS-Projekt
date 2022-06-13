import paho.mqtt.client as mqtt


class Publisher:
    mqtt_client: mqtt.Client

    def __init__(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("iot.soft.uni-linz.ac.at", 1883, 60)

    def send_on(self):
        self.mqtt_client.publish("camera/emergency-light", "ON")

    def send_off(self):
        self.mqtt_client.publish("camera/emergency-light", "OFF")
