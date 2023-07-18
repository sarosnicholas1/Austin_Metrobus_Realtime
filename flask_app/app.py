# save this as app.py
from flask import Flask, render_template, Response, send_file
import math
import json
from kafka import KafkaConsumer
import redis
import logging
from pykafka import KafkaClient
from datetime import datetime


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def hello():
    return send_file('templates/index.html')

@app.route("/stream")
def stream():
    
    def events():

        client = KafkaClient(hosts="127.0.0.1:9092")
        topic = client.topics['messages']
        consumer = topic.get_simple_consumer()

        #redis initalization
        r = redis.Redis(host='localhost', port=6379, db=1)
        
        for message in consumer:

            #decode message as readable json data
            string_data = message.value.decode('ascii')

            #loops through each vehicle dictionary in the data passed through kafka
            for vehicle in json.loads(string_data):
                
                # checks if not in database
                if not r.get(vehicle['id']):
                    r.set(vehicle['id'], json.dumps(vehicle))
                else:
                    prev_vehicle = json.loads(r.get(vehicle['id']))
                    speed = get_speed_mph(prev_vehicle['latitude'], prev_vehicle['longitude'], vehicle['latitude'], vehicle['longitude'])
                    app.logger.info(speed)

                yield f'data: {vehicle} \n\n'
               
    return Response(events(), mimetype="text/event-stream")



def get_speed_mph(lat1,long1,lat2,long2):

    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(long2-long1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    mph = ((d*1000)/8)*2.2
    return mph

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 
