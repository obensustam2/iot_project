Topic Publisher (Raspberry Pi-Python) -> MQTT Broker -> Topic Subscriber & InfluxDB Write (Python) -> Backend (Python) -> Frontend (Vue.js)

# Installations
## Mosquitto
```
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
sudo systemctl status mosquitto
```

## Python
```
cd iot_project/
pip3 install -r requirements.txt
```

## Frontend
```
cd iot_project/frontend/
npm i
```

# Run
## Python
```
cd iot_project/scripts/
python3 mqtt_publisher.py 
python3 mqtt_subscriber.py
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

## Frontend
```
cd iot_project/frontend/
npm run serve
```


