# VEDirectMQTT

A utility to ingest VE.Direct data from a Victron device and push it into an MQTT server. This will function similarly to the ClassicMQTT except that "modbus" is not needed to receive the data, it can be received using a simple VE.Direct to USB cable.

In this particular case we are seeking to place the data in the same MQTT instance that the ClassicMPPT uses, since this utility is part of the greater ClassicDIY universe. When the data is published in the MQTT instance, the readings will be under the following Topic:

VEDirectMQTT/\<device name>\/readings

Typically, the name of the device is something like BVM700, but you can configure this name so that if you have several Victron devices you can give them different names. If necessary, you can change the root as well because some MQTT services need you to publish under a certain root.

Only the Python implementation has been written so far and since the best interface cable for this device is the USB to VE.Direct cable made by Victron, I doubt if there ever will be an ESP implemetation, but there is a directory in ths repo if someone gets the urge or has a need.

The utiliy leverages the great work done in the vedirect library (https://github.com/karioja/vedirect.git) and, in fact, that library is a subproject to this GitHub repo. When you clone this repo, since it has a subproject. Use the following:

git clone --recursive git://github.com/ClassicDIY/VEDirectMQTT.git

So that the vedirect subproject will be populated.

If you are working with IOTstack, there is a compose_override.yml file included. You can copy that file into the IOTstack directory and then edit it for you particular installation and it will add this utility to the containers running in the IOTstack.

To get a great introduction and instructions on setting up IOTstack on your Raspberry Pi, see the Wiki for ClassicMQTT : https://github.com/ClassicDIY/ClassicMQTT/wiki/3.1-Raspberry-Pi-setup-using-IOTStack

When you get to step where you merge the compose-override.yml from ClassicMQTT, use this [compose-override.yml](./code/Python/compose-override.yml) included in this repo to add a container that will run VEDirectMQTT. (be sure to update it for your particular needs).