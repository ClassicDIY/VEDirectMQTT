
# VE.Direct MQTT Publisher Python Implementation


When it comes time to run the program, there are parameters that can be set or passed they are:
**Parameters:**
```  
--vedirect_name <BMV700>        : The name of the Victron device you are reading from, defaults to VBM700 if unspecified.  
--vedirect_port </dev/ttyUSB0>  : The name of the usb port the Victron device is plugged into. Defaults to /dev/ttyUSB0 if unspecified.  
--vedirect_timeout <60>         : The timeout for rading from the Victron device, defaults to 60 if unspecified.  
--mqtt <127.0.0.1>              : The IP or URL of the MQTT Broker, defaults to 127.0.0.1 if unspecified.  
--mqtt_port <1883>              : The port to you to connect to the MQTT Broker, defaults to 1883 if unspecified.  
--mqtt_root <ClassicMQTT>       : The root for your MQTT topics, defaults to ClassicMQTT if unspecified.  
--mqtt_user <username>          : The username to access the MQTT Broker.  
--mqtt_pass <password>          : The password to access the MQTT Broker.
--publish_rate <60>             : The amount of seconds between updates (default is 60 seconds).
```
