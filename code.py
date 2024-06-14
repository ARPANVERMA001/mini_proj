import pandas as pd  # for reading and manipulating data
import folium  # for plotting data on maps
import random  # random sampling
from geopy.distance import distance  # geo spatial distance computations
import requests  # for making API requests
from google.transit import gtfs_realtime_pb2  # for reading realtime GTFS data
from collections import defaultdict  # python's special dictionary data structure
import math
from datetime import datetime
import pytz
ist = pytz.timezone("Asia/Kolkata")
import time
# from ipyleaflet import Map, Marker, AntPath, Circle
from geopy.distance import geodesic
from app import create_app, db
from Model import RealtimeBus, Routes
from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError

app = create_app()
url = "https://bit.ly/gtfs-rt"

gtfs_files_dir = r"C:\msys64\mingw64\bin\PseudoGTFS\env\data\GTFS"
routes = pd.read_csv(gtfs_files_dir + r"\routes.txt")
trips = pd.read_csv(gtfs_files_dir + r"\trips.txt")
stops = pd.read_csv(gtfs_files_dir + r"\stops.txt")
stop_times = pd.read_csv(gtfs_files_dir + r"\stop_times.txt")
with app.app_context():
    def insert_realtime_data():
        try:#   realtime_data_dict = defaultdict(list)
            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get(url)
            feed.ParseFromString(response.content)
            for entity in feed.entity:
                vehicle_id = entity.vehicle.vehicle.id
                vehicle_timestamp = entity.vehicle.timestamp
                vehicle_lat = entity.vehicle.position.latitude
                vehicle_lon = entity.vehicle.position.longitude
                vehicle_route_id = int(float(entity.vehicle.trip.route_id))
                vehicle_trip_id = entity.vehicle.trip.trip_id
                vehicle_route_name = routes[routes.route_id == vehicle_route_id].route_long_name.squeeze()
                vehicle_datetime = datetime.fromtimestamp(vehicle_timestamp, ist)
                
                real_time_data = RealtimeBus(
                        vehicle_id=vehicle_id,
                        vehicle_timestamp=str(vehicle_timestamp),
                        vehicle_lat=vehicle_lat,
                        vehicle_lon=vehicle_lon,
                        vehicle_route_id=vehicle_route_id,
                        vehicle_trip_id=vehicle_trip_id,
                        vehicle_route_name=vehicle_route_name,
                        vehicle_datetime=vehicle_datetime
                    )
                db.session.add(real_time_data)
            db.session.commit()
        # except IntegrityError:
        #     db.session.rollback()
        #     print("Integrity error: There was an issue with inserting the data due to duplicate primary keys.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
    insert_realtime_data()
    # for i in range(5):
    #     insert_realtime_data()
    #     time.sleep(10)