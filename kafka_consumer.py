from confluent_kafka import Consumer
import requests
import json

QDRANT_URL = "http://localhost:6333/collections/air_quality/points"

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'env_group',
    'auto.offset.reset': 'earliest'
})

def create_collection():
    url = "http://localhost:6333/collections/air_quality"
    data = {
        "vectors": {
            "size": 5,
            "distance": "Cosine"
        }
    }
    requests.put(url, json=data)

create_collection()

consumer.subscribe(['env_data'])

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    data = json.loads(msg.value().decode('utf-8'))

    vector = [
        data.get('pm25', 0.0) or 0.0,
        data.get('pm10', 0.0) or 0.0,
        data.get('co2', 0.0) or 0.0,
        data.get('temp', 0.0) or 0.0,
        data.get('humidity', 0.0) or 0.0
    ]

    payload = {
        "points": [{
            "id": int(data['timestamp']),
            "vector": vector,
            "payload": data
        }]
    }

    r = requests.put(QDRANT_URL, json=payload)
    print(f"Added point, status: {r.status_code}, response: {r.text}")

consumer.close()
