from fetch_data import get_data
from kafka import KafkaProducer
import time
import json
from pykafka import KafkaClient


def serializer(message):
    serialized_data = json.dumps(message).encode('utf-8')
    return serialized_data

"""
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

if __name__ == '__main__':

    for i in range(20):
        dummy_message = get_data()
        print("message sent:" + str(i))
        producer.send('messages', dummy_message)
        time.sleep(5)

"""
client = KafkaClient(hosts="127.0.0.1:9092")
topic = client.topics['messages']

with topic.get_sync_producer() as producer:
        for i in range(40):
            data = get_data()
            message = str(data).encode('ascii')
            producer.produce(message)
            print("message sent")
            time.sleep(8)