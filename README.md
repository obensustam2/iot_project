Topic Publisher (Raspberry Pi-Python) -> MQTT Broker -> Topic Subscriber & InfluxDB Write (Python) -> Backend (Python) -> Frontend (Vue.js)

# Installations
```
pip3 install paho-mqtt
pip3 install influxdb-client
pip3 install fastapi uvicorn
```

# Run
## Frontend
```
cd iot_project/frontend/
npm run serve
```

## Scripts
```
cd iot_project/scripts/
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
python3 mqtt_publisher.py 
python3 mqtt_subscriber.py
```
