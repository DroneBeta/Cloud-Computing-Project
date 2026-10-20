import time, json, random, ssl
import paho.mqtt.client as mqtt

#____________________________________________________________________________
# This simulating aims to create data as there is no sensor collecting data.
# 
# 1. Defines all ports addresses/values
# 2. Create the paho instance, the third party mqtt used, & connects to it
# 3. Define the sensors, can be further expanded if needed
# 4. In the while loop, create a payload that create all data + the fabricated
# example data with timers to not overload the mqtt
#____________________________________________________________________________


broker = "broker.hivemq.com"
port = 8883
topic = "air/sensor"

client = mqtt.Client()
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.tls_insecure_set(False)
client.connect(broker, port)

sensors = [
    {"device_id": "sensor_berlin_center", "latitude": 52.520, "longitude": 13.405},  # Berlin Mitte
    {"device_id": "sensor_berlin_north", "latitude": 52.567, "longitude": 13.415},   # Prenzlauer Berg
    {"device_id": "sensor_berlin_south", "latitude": 52.457, "longitude": 13.381},   # Tempelhof
]

while True:
    for sensor in sensors:
        payload = {
            "device_id": sensor["device_id"],
            "pm25_level": round(random.uniform(0.0, 150.0), 2), # Generate fake PM2.5 air quality reading (µg/m³)
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "latitude": sensor["latitude"],
            "longitude": sensor["longitude"]
        }
        print("Sending:", payload)
        client.publish(topic, json.dumps(payload))
        time.sleep(2)
    time.sleep(5)
