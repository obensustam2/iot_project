from fastapi import FastAPI
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
from fastapi.middleware.cors import CORSMiddleware

# InfluxDB v2 settings
influx_url = "YOUR_URL"
influx_token = "YOUR_TOKEN"
influx_org = "YOUR_ORGANIZATION"
influx_bucket = "YOUR_BUCKET"  

# Setup InfluxDB client
client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
query_api = client.query_api()

# Setup FastAPI app
app = FastAPI()

# Enable CORS so frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/temperature")
def get_recent_temperatures_grouped():
    query = f'''
        from(bucket: "{influx_bucket}")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "temperature")
        |> filter(fn: (r) => r._field == "value")
        |> filter(fn: (r) => r.device != "esptemp03" and r.device != "esptemp04")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 100)
    '''

    result = query_api.query(org=influx_org, query=query)

    grouped_data = {}
    for table in result:
        for record in table.records:
            device = record.values.get("device", "unknown")
            entry = {
                "temperature": record.get_value(),
                "time": str(record.get_time())
            }
            if device not in grouped_data:
                grouped_data[device] = []
            grouped_data[device].append(entry)

    return grouped_data


