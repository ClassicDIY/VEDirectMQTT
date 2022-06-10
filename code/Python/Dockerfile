FROM python:3.7.6-slim-stretch

RUN pip install --no-cache-dir paho-mqtt pyserial

ADD vedirect_mqtt.py /
ADD support/*.py support/
ADD vedirect/ vedirect/

ENTRYPOINT ["python3", "vedirect_mqtt.py"]
