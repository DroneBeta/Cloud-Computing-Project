import base64, json
from google.cloud import bigquery

#____________________________________________________________________________
# This function is deployed onto the google cloud, allowing 
# the developers to program task for the cloud to do automatically.
# 
# 1. Define the function
# 2. Receive the payload (all the data published from the mqtt) &
# decodes the Pub/Sub message
# 3. Process the pm25 into a boolean value named anomaly
# 4. Connect to the BigQuerry to gain access to the data table
# 5. Logs all data
#____________________________________________________________________________

def process_data(event, context):
    payload = base64.b64decode(event['data']).decode('utf-8')
    data = json.loads(payload)

    device_id = data.get("device_id", "unknown")
    pm25 = float(data.get("pm25_level", 0))
    timestamp = data.get("timestamp")
    lat = float(data.get("latitude", 0))
    lon = float(data.get("longitude", 0))

    anomaly = pm25 > 35.0  # WHO unsafe PM2.5 threshold

    client = bigquery.Client(project="air-quality-berlin")  
    table_id = "air-quality-berlin.air_readings.air_readings_table"

    rows = [{
        "device_id": device_id,
        "pm25_level": pm25,
        "timestamp": timestamp,
        "anomaly": anomaly,
        "latitude": lat,
        "longitude": lon
    }]

    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"Error inserting into BigQuery: {errors}")
    else:
        print(f"Data inserted: {rows}")
