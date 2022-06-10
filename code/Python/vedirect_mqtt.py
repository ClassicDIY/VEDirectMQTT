#!/usr/bin/python3
from paho.mqtt import client as mqttclient
from vedirect.vedirect import Vedirect
from collections import OrderedDict
import json
import time
import socket
import threading
import logging
import os
import sys
from random import randint, seed
from enum import Enum

from support.vedirect_validate import handleArgs
from time import time_ns


# --------------------------------------------------------------------------- # 
# GLOBALS
# --------------------------------------------------------------------------- # 
MAX_RATE                    = 600       #in seconds
MIN_RATE                    = 15        #in seconds
DEFAULT_RATE                = 60        #in seconds
MQTT_MAX_ERROR_COUNT        = 300       #Number of errors on the MQTT before the tool exits
MAIN_LOOP_SLEEP_SECS        = 5         #Seconds to sleep in the main loop

# --------------------------------------------------------------------------- # 
# Default startup values. Can be over-ridden by command line options.
# --------------------------------------------------------------------------- # 
argumentValues = { \
    'vedirectName':os.getenv('VEDIRECT_HOST', "VDM700"), \
    'vedirectPort':os.getenv('VEDIRECT_PORT', "/tty/devUSB0"), \
    'vedirectTimeout':os.getenv('VEDIRECT_TIMEOUT', "60"), \
    'mqttHost':os.getenv('MQTT_HOST', "127.0.0.1"), \
    'mqttPort':os.getenv('MQTT_PORT', "1883"), \
    'mqttRoot':os.getenv('MQTT_ROOT', "ClassicMQTT"), \
    'mqttUser':os.getenv('MQTT_USER', "ClassicPublisher"), \
    'mqttPassword':os.getenv('MQTT_PASS', "ClassicPub123"), \
    'publishRate':int(os.getenv('PUBLISH_RATE', str(DEFAULT_RATE)))}

# --------------------------------------------------------------------------- # 
# Counters and status variables
# --------------------------------------------------------------------------- # 
infoPublished               = False
mqttConnected               = False
doStop                      = False
modeAwake                   = False

mqttErrorCount              = 0
currentPollRate             = DEFAULT_RATE
mqttClient                  = None

# --------------------------------------------------------------------------- # 
# configure the logging
# --------------------------------------------------------------------------- # 
log = logging.getLogger('vedirect_mqtt')
if not log.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler) 
    log.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))

# --------------------------------------------------------------------------- # 
# MQTT On Connect function
# --------------------------------------------------------------------------- # 
def on_connect(client, userdata, flags, rc):
    global mqttConnected, mqttErrorCount, mqttClient
    if rc==0:
        mqttConnected = True
        mqttErrorCount = 0
    else:
        mqttConnected = False
        log.error("MQTT Bad connection Returned code={}".format(rc))

# --------------------------------------------------------------------------- # 
# MQTT On Disconnect
# --------------------------------------------------------------------------- # 
def on_disconnect(client, userdata, rc):
    global mqttConnected, mqttClient
    mqttConnected = False
    #if disconnetion was unexpectred (not a result of a disconnect request) then log it.
    if rc!=mqttclient.MQTT_ERR_SUCCESS:
        log.debug("on_disconnect: Disconnected. ReasonCode={}".format(rc))

# --------------------------------------------------------------------------- # 
# MQTT Publish the data
# --------------------------------------------------------------------------- # 
def mqttPublish(client, data, subtopic):
    global mqttConnected, mqttErrorCount

    topic = "{}{}/{}".format(argumentValues['mqttRoot'], argumentValues['vedirectName'], subtopic)
    log.debug("Publishing: {}".format(topic))
    
    try:
        client.publish(topic,data)
        return True
    except Exception as e:
        log.error("MQTT Publish Error Topic:{}".format(topic))
        log.exception(e, exc_info=True)
        mqttConnected = False
        return False


def vedirect_rx_callback(packet):
    global mqttClient, mqttErrorCount, currentPollRate

    timePassed = ((time_ns()/1000000000.0) - beforeTime)

    try:
        if timePassed > currentPollRate:
            if mqttPublish(mqttClient,packet,"readings"):
                beforeTime = time_ns() /  1000000000.0
            else:
                mqttErrorCount += 1

    except Exception as e:
        log.error("Caught Error in periodic")
        log.exception(e, exc_info=True)


# --------------------------------------------------------------------------- # 
# Main
# --------------------------------------------------------------------------- 

def run(argv):

    global doStop, mqttClient

    log.info("vedirect_mqtt starting up...")

    handleArgs(argv, argumentValues)

    #random seed from the OS
    seed(int.from_bytes( os.urandom(4), byteorder="big"))

    mqttErrorCount = 0

    #setup the MQTT Client for publishing and subscribing
    clientId = argumentValues['mqttUser'] + "_mqttclient_" + str(randint(100, 999))
    log.info("Connecting with clientId=" + clientId)
    mqttClient = mqttclient.Client(clientId) 
    mqttClient.username_pw_set(argumentValues['mqttUser'], password=argumentValues['mqttPassword'])
    mqttClient.on_connect = on_connect    
    mqttClient.on_disconnect = on_disconnect  
    #mqttClient.on_message = on_message

    #Set Last Will 
    will_topic = "{}{}/tele/LWT".format(argumentValues['mqttRoot'], argumentValues['vedirectName'])
    mqttClient.will_set(will_topic, payload="Offline", qos=0, retain=False)

    try:
        log.info("Connecting to MQTT {}:{}".format(argumentValues['mqttHost'], argumentValues['mqttPort']))
#        mqttClient.connect(host=argumentValues['mqttHost'],port=int(argumentValues['mqttPort'])) 
        mqttClient.connect(host='remotepi.glaserisland.pertino.net',port=1883) 
    except Exception as e:
        log.error("Unable to connect to MQTT, exiting...")
        sys.exit(2)

    ve = Vedirect(argumentValues['vedirectPort'], argumentValues['vedirectTimeout'])

    mqttClient.loop_start()


    # start receiving the VE.Direct data.
    ve.read_data_callback(vedirect_rx_callback)

    log.debug("Starting main loop...")
    while not doStop:
        try:            
            time.sleep(MAIN_LOOP_SLEEP_SECS)

            if not mqttConnected:
                if (mqttErrorCount > MQTT_MAX_ERROR_COUNT):
                    log.error("MQTT Error count exceeded, disconnected, exiting...")
                    doStop = True

        except KeyboardInterrupt:
            log.error("Got Keyboard Interuption, exiting...")
            doStop = True
        except Exception as e:
            log.error("Caught other exception...")
            log.exception(e, exc_info=True)
    
    log.info("Exited the main loop, stopping other loops")
    log.info("Stopping MQTT loop...")
    mqttClient.loop_stop()

    log.info("Exiting vedirect_mqtt")

if __name__ == '__main__':
    run(sys.argv[1:])