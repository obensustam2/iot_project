import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# MQTT settings
broker = "test.mosquitto.org"
port = 1883
topic = "sensors/+/temperature"  # Wildcard subscription

# InfluxDB v2 settings
influx_url = "https://us-east-1-1.aws.cloud2.influxdata.com"
influx_token = "4HjjupLgkVgu9BabBEmNVWUprVLHmXZPRr1mokHFmmEvKiaaz1P_NyFMWLO9eOgihBNFuDDSYcq6Efyn8_cjdQ=="
influx_org = "DIY Team"
influx_bucket = "_monitoring"  

# Initialize InfluxDB client
influx_client = InfluxDBClient(url=influx_url,token=influx_token,org=influx_org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT broker with result code", rc)
    client.subscribe(topic)
    print("📡 Subscribed to topic:", topic)

def on_message(client, userdata, msg):
    try:
        temperature = float(msg.payload.decode())
        topic_parts = msg.topic.split('/')
        device_id = topic_parts[1] if len(topic_parts) >= 3 else "unknown"

        print(f"📥 {device_id}: {temperature} °C")

        point = Point("temperature") \
            .tag("device", device_id) \
            .field("value", temperature)

        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        print(f" Written to InfluxDB for device: {device_id}")

    except Exception as e:
        print("❌ Error processing message:", e)

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever()
