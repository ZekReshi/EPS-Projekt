import paho.mqtt.client as mqtt
import vehicledetectionmessage_pb2


if __name__ == '__main__':
    proto_msg = vehicledetectionmessage_pb2.PBMessage()
    proto_msg.control.action = vehicledetectionmessage_pb2.Action.OFF
    print(proto_msg.SerializeToString())
    client = mqtt.Client()
    client.connect("iot.soft.uni-linz.ac.at", 1883, 60)
    ret = client.publish("emergencyvehicledetection", proto_msg.SerializeToString())
    client.disconnect()#publishclient.