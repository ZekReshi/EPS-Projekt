#!/usr/bin/python

from __future__ import division
import time
import paho.mqtt.client as mqtt
import vehicledetectionmessage_pb2
import logging


class Actuator:

    def __init__(self, call_back):
        self.client = mqtt.Client()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level="INFO")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.call_back = call_back

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("camera/emergency-light", qos=0)
        self.logger.info('Connected with result code %s', str(rc))

    def on_message(self, client, userdata, msg):
        commandString = str(msg.payload)
        proto_msg = vehicledetectionmessage_pb2.PBMessage()
        try:
            proto_msg.ParseFromString(msg.payload)

            if proto_msg.HasField('control'):
                self.logger.debug('got message at %s with content %s', str(msg.topic), commandString)
                self.logger.info('got message from %s (with target %s)', proto_msg.source, proto_msg.target)
                self.logger.info('action numeric %s', proto_msg.control.action)
                self.logger.info('action Info %s', vehicledetectionmessage_pb2.Action.Name(proto_msg.control.action))
                self.call_back(proto_msg.control.action)
            else:
                self.logger.warning('got message at %s with content %s', str(msg.topic), commandString)

        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print(e)
            self.logger.warning('Unable to decode message: No valid ProtoBuf Msg received')



    def on_run(self):
        self.client.connect("iot.soft.uni-linz.ac.at", 1883, 60)
        try:
            self.client.loop_forever()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info('disconnecting ...')
            self.client.disconnect()
            time.sleep(1)
