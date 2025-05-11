import paho.mqtt.client as mqtt
import random
import time

# MQTT broker settings
broker = "test.mosquitto.org"
port = 1883

# Topic
topic = "sensors/laptop002/temperature"

client = mqtt.Client()
client.connect(broker, port, 60)

while True:
    temp = round(random.uniform(0.0, 5.0), 2)
    client.publish(topic, str(temp))
    print("Published:", temp)
    time.sleep(5)

    
