FROM python:3.7.6-slim-stretch

RUN pip install --no-cache-dir pymodbus paho-mqtt

ADD VEDirectMQTT.py /
ADD support/*.py support/

ENTRYPOINT ["python3", "VEDirectMQTT.py"]