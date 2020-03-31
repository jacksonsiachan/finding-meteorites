#! /usr/bin/env python3

import math
import requests

def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
      math.cos(lat1) * \
      math.cos(lat2) * \
      math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

def get_dist(meteor):
    return meteor.get('distance', math.inf)    

if __name__ == '__main__':
    meteor_resp = requests.get('https://data.nasa.gov/resource/gh4g-9sfh.json')
    meteor_data = meteor_resp.json()
    my_location = (1.289437,103.84998) # SG Lat and Long

    for meteor in meteor_data:
        if 'reclat' not in meteor or 'reclong' not in meteor: 
            continue
        meteor["distance"] = calc_dist(float(meteor['reclat']), float(meteor['reclong']), my_location[0], my_location[1])

    meteor_data.sort(key=get_dist)    
    print(meteor_data[0]) # Meteor landing that is closest to Singapore.

    print(len(meteor_data)) # Total number of data

    print(len([ m for m in meteor_data if 'distance' not in m ])) # number of data without distance 