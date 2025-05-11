from fastapi import FastAPI
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
from fastapi.middleware.cors import CORSMiddleware

# InfluxDB v2 settings
influx_url = "https://us-east-1-1.aws.cloud2.influxdata.com"
influx_token = "4HjjupLgkVgu9BabBEmNVWUprVLHmXZPRr1mokHFmmEvKiaaz1P_NyFMWLO9eOgihBNFuDDSYcq6Efyn8_cjdQ=="
influx_org = "DIY Team"
influx_bucket = "_monitoring"

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

