# For testing purposes
import time
import paho.mqtt.client as mqtt


# mqtt connect callback function
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("camera/emergency-light", qos=0)


# mqtt message received callback function
def on_message(client, userdata, msg):
    message_string = str(msg.payload.decode("utf-8"))
    print(message_string)


# setup mqtt
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# connect mqtt
mqtt_client.connect("iot.soft.uni-linz.ac.at", 1883, 60)
try:
    mqtt_client.loop_forever()
except (KeyboardInterrupt, SystemExit):
    mqtt_client.disconnect()
    time.sleep(1)
