
# VE.Direct MQTT Publisher Python Implementation

This is a utility intended to recive the data from a VE.Direct device and post the data into an MQTT instance. In this particular case we are seeking to place the data in the same MQTT instance that the ClassicMPPT uses, since this utility is part of the greater ClassicDIY universe.

The intent of this utility is to put the data in an MQTT instance. If you do not know what that is or need help in this area, there are a ton of places to learn about it. Start with ClassicDIY or IOTstack and go from there.

When it comes time to run the program, there are parameters that can be set or passed they are:
**Parameters:**
```  
--vedirect_name <BMV700>        : The name of the Victron device you are reading from, defaults to VBM700 if unspecified.  
--vedirect_port </dev/ttyUSB0>  : The name of the usb port the Victron device is plugged into. Defaults to /dev/ttyUSB0.  
--vedirect_timeout <60>         : The timeout for rading from the Victron device, defaults to 60 if unspecified.  
--publish_rate <15>             : The amount of seconds between updates (default is 15 seconds).
--mqtt <127.0.0.1>              : The IP or URL of the MQTT Broker, defaults to 127.0.0.1 if unspecified.  
--mqtt_port <1883>              : The port to you to connect to the MQTT Broker, defaults to 1883 if unspecified.  
--mqtt_root <VEDirectMQTT>      : The root for your MQTT topics, defaults to VEDirectMQTT if unspecified.  
--mqtt_user <username>          : The username to access the MQTT Broker.  
--mqtt_pass <password>          : The password to access the MQTT Broker.
```
