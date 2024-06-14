# Defining the Model for the db
from app import db
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Routes(db.Model):
    __tablename__ = 'Routes'

    agency_id = db.Column(db.Text, nullable=False)
    route_id = db.Column(db.Integer, primary_key=True, nullable = False)
    route_long_name = db.Column(db.Text, nullable=False)
    route_short_name = db.Column(db.Text, nullable=True)
    route_type = db.Column(Enum('0', '1', '2', '3', '4', '5', '6', '7', '11', '12'), nullable=False)

    # trips = relationship("Trips", back_populates="route")

    def __repr__(self):
        return f'{self.route_id}'
    
    def to_dict(self):
        return {
            'agency_id': self.agency_id,
            'route_id': self.route_id,
            'route_long_name': self.route_long_name,
            'route_short_name': self.route_short_name,
            'route_type': self.route_type
        }

class Stops(db.Model):
    __tablename__ = 'Stops'

    stop_id = db.Column(db.Integer, primary_key=True)
    stop_code = db.Column(db.Text, nullable=False)
    stop_lat = db.Column(db.Float, nullable=False)
    stop_lon = db.Column(db.Float, nullable=False)
    stop_name = db.Column(db.Text, nullable=False)

    # stop_times = relationship("StopTimes", back_populates="stop")

    def __repr__(self):
        return f'{self.stop_id}'
    
    def to_dict(self):
        return {
            'stop_id': self.stop_id,
            'stop_code': self.stop_code,
            'stop_lat': self.stop_lat,
            'stop_lon': self.stop_lon,
            'stop_name': self.stop_name
        }

class Trips(db.Model):
    __tablename__ = 'Trips'

    trip_id = db.Column(db.Text, primary_key=True)
    route_id = db.Column(db.Integer, nullable=False) #, ForeignKey('Routes.route_id')
    service_id = db.Column(db.Text, nullable=False)
    shape_id = db.Column(db.Text, nullable=True)

    # route = relationship('Routes', back_populates='trips')
    # stop_times = relationship('StopTimes', back_populates='trip')

    def __repr__(self):
        return f'{self.trip_id}'

    def to_dict(self):
        return {
            'trip_id': self.trip_id,
            'route_id': self.route_id,
            'service_id': self.service_id,
            'shape_id': self.shape_id
        }

class StopTimes(db.Model):
    __tablename__ = 'StopTimes'

    trip_id = db.Column(db.Text, primary_key=True) #, ForeignKey('Trips.trip_id')
    stop_sequence = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer) #, ForeignKey('Stops.stop_id')
    arrival_time = db.Column(db.Text, nullable=False)
    departure_time = db.Column(db.Text, nullable=False)

    # trip = relationship('Trips', back_populates='stop_times')
    # stop = relationship('Stops', back_populates='stop_times')
    def __repr__(self):
        return f'{self.trip_id} - {self.stop_id}'
    
    def to_dict(self):
        return {
            'trip_id': self.trip_id,
            'stop_sequence': self.stop_sequence,
            'stop_id': self.stop_id,
            'arrival_time': self.arrival_time,
            'departure_time': self.departure_time
        }

class RealtimeBus(db.Model):
    __tablename__ = 'RealtimeBus'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    vehicle_id = db.Column(db.Text, nullable = False)
    vehicle_timestamp = db.Column(db.Text, nullable = False)
    vehicle_lat = db.Column(db.Float, nullable=False)
    vehicle_lon = db.Column(db.Float, nullable=False)
    vehicle_route_id = db.Column(db.Text, nullable=False)
    vehicle_trip_id = db.Column(db.Text, nullable=False)
    vehicle_route_name = db.Column(db.Text, nullable=False)
    vehicle_datetime = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'vehicle_id: {self.vehicle_id} date_time:{self.vehicle_datetime}'

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'vehicle_timestamp': self.vehicle_timestamp,
            'vehicle_lat': self.vehicle_lat,
            'vehicle_lon': self.vehicle_lon,
            'vehicle_route_id': self.vehicle_route_id,
            'vehicle_trip_id': self.vehicle_trip_id,
            'vehicle_route_name': self.vehicle_route_name,
            'vehicle_datetime': self.vehicle_datetime
        }
    
    def get_vehicle_datetime(self):
        return datetime.strptime(self.vehicle_datetime, '%Y-%m-%d %H:%M:%S')