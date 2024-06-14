# Inserts all the Routes and Stops data into db
from app import create_app, db
from Model import Routes, Stops, StopTimes, Trips
import os, csv

temp_test_instance = create_app()

# Adds Routes Data:
def read_routes_data(file_path):
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            fields = line.strip().split(',')
            agency_id = fields[0]
            route_id = int(fields[1])
            route_long_name = fields[2]
            route_short_name = fields[3]
            route_type = fields[4]

            route = Routes(
                agency_id=agency_id,
                route_id=route_id,
                route_long_name=route_long_name,
                route_short_name=route_short_name,
                route_type=route_type
            )

            db.session.add(route)
        db.session.commit()

# Adds Stops Data:
def insert_stops_data(file_path):
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            fields = line.strip().split(',')
            stop_code, stop_id, stop_lat, stop_lon, stop_name = fields

            stop = Stops(
                stop_id=int(stop_id),
                stop_code=stop_code,
                stop_lat=float(stop_lat),
                stop_lon=float(stop_lon),
                stop_name=stop_name
            )
            db.session.add(stop)
        db.session.commit()

# Add STopTimesData: 
def read_stop_times_data(file_path):
    app = create_app()
    with app.app_context():
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stop_time = StopTimes(
                    trip_id=row['trip_id'],
                    stop_sequence=row['stop_sequence'],
                    stop_id=row['stop_id'],
                    arrival_time=row['arrival_time'],
                    departure_time=row['departure_time']
                )
                db.session.add(stop_time)
            db.session.commit()

# Add Trips Data:
def read_trips_data(file_path):
    app = create_app()
    with app.app_context():
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                trip = Trips(
                    trip_id=row['trip_id'],
                    route_id=row['route_id'],
                    service_id=row['service_id'],
                    shape_id=row.get('shape_id')  # shape_id can be None
                )
                db.session.add(trip)
            db.session.commit()

with temp_test_instance.app_context():
    file_path = os.path.join(os.path.dirname(__file__), 'data/GTFS/routes.txt')
    read_routes_data(file_path)
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'GTFS', 'stops.txt')
    insert_stops_data(file_path)
    file_path = os.path.join(os.path.dirname(__file__), 'data/GTFS/routes.txt')

    file_path = "C:/msys64/mingw64/bin/PseudoGTFS/env/data/GTFS/stop_times.txt"
    read_stop_times_data(file_path)
    file_path = "C:/msys64/mingw64/bin/PseudoGTFS/env/data/GTFS/trips.txt"
    read_trips_data(file_path)