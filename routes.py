# Routes for Endpoints!
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import threading
import time
import requests
from google.transit import gtfs_realtime_pb2
import pandas as pd
from Model import Routes, Stops, Trips, StopTimes, RealtimeBus
from sqlalchemy.exc import IntegrityError
import pytz

gtfs_files_dir = r"C:\msys64\mingw64\bin\PseudoGTFS\env\data\GTFS"
routes = pd.read_csv(gtfs_files_dir + r"\routes.txt")
trips = pd.read_csv(gtfs_files_dir + r"\trips.txt")
stops = pd.read_csv(gtfs_files_dir + r"\stops.txt")
stop_times = pd.read_csv(gtfs_files_dir + r"\stop_times.txt")

ist = pytz.timezone("Asia/Kolkata")

fetch_thread = None
stop_thread = False

# This structure has both get_realtime_data and insert_realtime_data in it!!
def register_routes(app, db):
    def get_realtime_data_route(last_min=5):
        now = datetime.now()
        delta = now - timedelta(minutes=last_min)
        realtime_data = RealtimeBus.query.filter(
            RealtimeBus.vehicle_datetime >= delta.strftime('%Y-%m-%d %H:%M:%S'),
            RealtimeBus.vehicle_datetime <= now.strftime('%Y-%m-%d %H:%M:%S')
        ).all()
        return jsonify([data.to_dict() for data in realtime_data])

    def insert_realtime_data():
        try:
            url = "https://bit.ly/gtfs-rt"
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
        except IntegrityError:
            db.session.rollback()
            print("Integrity error: There was an issue with inserting the data due to duplicate primary keys.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")

    def fetch_and_store_data():
        global stop_thread
        while not stop_thread:
            with app.app_context():
                insert_realtime_data()
            time.sleep(10)

    # Route to get realtime_data, takes 5 min as default!
    @app.route('/realtime_query', methods=['GET'])
    def realtime_query():
        last_min = request.args.get('last_min', default=5, type=int)
        return get_realtime_data_route(last_min)
    
    # Route to get the Routes data
    @app.route('/routes', methods=['GET'])
    def get_routes():
        routes = Routes.query.all()
        # return jsonify([route.__repr__() for route in routes])
        return jsonify([route.to_dict() for route in routes])

    # Route to get stops data
    @app.route('/stops', methods=['GET'])
    def get_stops():
        stops = Stops.query.all()
        # return jsonify([stop.__repr__() for stop in stops])
        return jsonify([stop.to_dict() for stop in stops])

    # Rotue to get the stop_times data
    @app.route('/stop_times', methods=['GET'])
    def get_stop_times():
        stop_times = StopTimes.query.all()
        # return jsonify([stop.__repr__() for stop in stop_times])
        return jsonify([stop.to_dict() for stop in stop_times])
    
    # Route to get the trips data
    @app.route('/trips', methods=['GET'])
    def get_trips():
        trips = Trips.query.all()
        # return jsonify([trip.__repr__() for trip in trips])
        return jsonify([trip.to_dict() for trip in trips])

    # Route to get the stops_on_route 
    @app.route('/stops_on_route', methods=['GET'])
    def get_stops_on_route():
        route_id = request.args.get('route_id', default=1, type=int)
        stops_on_route = (
            db.session.query(Stops)
            .join(StopTimes, Stops.stop_id == StopTimes.stop_id)
            .join(Trips, StopTimes.trip_id == Trips.trip_id)
            .join(Routes, Trips.route_id == Routes.route_id)
            .filter(Routes.route_id == route_id)
            .order_by(StopTimes.stop_sequence)
            .all()
        )
        return jsonify([f"Stop ID: {stop.stop_id}, Stop Name: {stop.stop_name}, Stop Lat: {stop.stop_lat}, Stop Lon: {stop.stop_lon}" for stop in stops_on_route])

    # Route for inserting data into db.
    # Two action commands 'start' and 'stop'

    @app.route('/insert_data', methods=['GET'])
    def insert_data():
        global fetch_thread, stop_thread
        action = request.args.get('action')
        if action == 'start':
            if fetch_thread is None or not fetch_thread.is_alive():
                stop_thread = False
                fetch_thread = threading.Thread(target=fetch_and_store_data)
                fetch_thread.daemon = True
                fetch_thread.start()
                return 'Data fetching started', 200
            else:
                return 'Data fetching is already running', 200
        elif action == 'stop':
            stop_thread = True
            if fetch_thread is not None:
                fetch_thread.join()
                fetch_thread = None
            return 'Data fetching stopped', 200
        return 'Invalid action', 400