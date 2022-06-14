#!/usr/bin/python

from __future__ import division
import time
import paho.mqtt.client as mqtt
import logging
from at.jku.pervasive.eps.mymqttmessages.mymqttmessages_pb2 import *


class Actuator:

    def __init__(self, call_back):
        self.client = mqtt.Client()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level="INFO")
        self.client.on_connect = self.on_connect
        self.client.on_message = call_back

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info('Connected with result code %s', str(rc))
        client.subscribe("emergencyvehicledetection", qos=0)


    def on_run(self):
        self.client.connect("iot.soft.uni-linz.ac.at", 1883, 60)
        try:
            self.client.loop_forever()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info('disconnecting ...')
            self.client.disconnect()
            time.sleep(1)


# mqtt message received callback function



# setup mqtt


# connect mqtt
