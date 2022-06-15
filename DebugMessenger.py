import paho.mqtt.client as mqtt
import vehicledetectionmessage_pb2
import random
import time
if __name__ == '__main__':

    client = mqtt.Client()
    client.connect("iot.soft.uni-linz.ac.at", 1883, 60)
    try:
        while True:
            rand = random.choices([0,1],weights = (20,70), k =1)

            proto_msg = vehicledetectionmessage_pb2.PBMessage()
            proto_msg.control.action = rand[0]
            print("Sending "+ vehicledetectionmessage_pb2.Action.Name(proto_msg.control.action))
            ret = client.publish("emergencyvehicledetection", proto_msg.SerializeToString())
            time.sleep(1)
    except KeyboardInterrupt:
        print('stopped')



    client.disconnect()