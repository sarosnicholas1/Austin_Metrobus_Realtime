#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
import requests


def get_data():
    x = requests.get('https://data.texas.gov/download/cuc7-ywmd/text/plain')
    data = x.json()
    df = pd.json_normalize(data['entity'])


    #dropping unnessasary columns
    df = df.drop([
            'vehicle.trip.tripId',
            'vehicle.trip.startDate',
            'vehicle.position.speed', 
            'vehicle.currentStopSequence',
            'vehicle.stopId',
            'vehicle.vehicle.id', 
            'vehicle.vehicle.label',
            'vehicle.vehicle.licensePlate'
            ], axis=1)

    #relabeling dataframe
    new_cols = ["id", "route_id", "latitude", "longitude", "timestamp", "bearing", "current_status"]
    df.columns = new_cols
    df.fillna(0, inplace = True)


    #only contains high frequencey routes
    high_freq_routes = ["2", "4", "7", "10", "18", "20", "300", "311", "325", "333", "335"]
    df = df[df.route_id.isin(high_freq_routes)].reset_index(drop=True)
    

    json_data = df.to_json(orient='records')
    return json_data



