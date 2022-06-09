#! /bin/bash

#set the ENV variables that the script uses
#export LOGFILE="/log/vedirectmqtt.log"
#export LOGLEVEL=DEBUG

#This scrip just sets the ENV variables and runs the script.

python3 ./VEDirectMQTT.py --mqtt 127.0.0.1 --mqtt_port 1883 --mqtt_root VEDirectMQTT --mqtt_user ClassicPublisher --mqtt_pass ClassicPub123
