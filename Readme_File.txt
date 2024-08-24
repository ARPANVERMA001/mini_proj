# Real-time Bus Tracking Application

This Flask-based application tracks real-time bus locations in Delhi using GTFS (General Transit Feed Specification) data and real-time updates from Delhi's Open Transit Data API.

## Features

- **Fetches and Stores GTFS Data:** Includes routes, stops, trips, and stop times.
- **Retrieves Real-time Bus Location Updates:** Provides up-to-date location data for buses.
- **API Endpoints:** For querying bus data.
- **Database Integration:** Stores data in an SQLite database using SQLAlchemy ORM.

## SQLite Database Schema

The application uses the following database schema to store GTFS and real-time bus data:

### Tables

- **Routes:** Stores route information.
  - `agency_id` (Text)
  - `route_id` (Integer, Primary Key)
  - `route_long_name` (Text)
  - `route_short_name` (Text)
  - `route_type` (Enum)
  
- **Stops:** Stores stop details.
  - `stop_id` (Integer, Primary Key)
  - `stop_code` (Text)
  - `stop_lat` (Float)
  - `stop_lon` (Float)
  - `stop_name` (Text)
  
- **Trips:** Stores trip information.
  - `trip_id` (Text, Primary Key)
  - `route_id` (Integer)
  - `service_id` (Text)
  - `shape_id` (Text)
  
- **StopTimes:** Stores stop times for trips.
  - `trip_id` (Text, Primary Key)
  - `stop_sequence` (Integer, Primary Key)
  - `stop_id` (Integer)
  - `arrival_time` (Text)
  - `departure_time` (Text)
  
- **RealtimeBus:** Stores real-time bus location data.
  - `id` (Integer, Primary Key, Auto-increment)
  - `vehicle_id` (Text)
  - `vehicle_timestamp` (Text)
  - `vehicle_lat` (Float)
  - `vehicle_lon` (Float)
  - `vehicle_route_id` (Text)
  - `vehicle_trip_id` (Text)
  - `vehicle_route_name` (Text)
  - `vehicle_datetime` (Text)

## Getting Started

### Prerequisites

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Requests
- Google Protobuf (for GTFS Realtime)

### Installation

1. **Clone the repository:**
   git clone https://github.com/yourusername/realtime-bus-tracking.git
   cd realtime-bus-tracking
2. **Create a virtual env and activate it:**
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
3. **Install the required dependencies:**
   pip install -r requirements.txt
4. **Initialize the database:**
   flask db init
   flask db migrate
   flask db upgrade

### Running the Application
**Start the flask application:**
  python run.py
  Access the application at http://localhost:5000.

### API Endpoints
1. **Start inserting real-time data into the database:**
   GET /insert_data?action=start
2. **Stop inserting real-time data into the database:**
   GET /insert_data?action=stop
3. **Get real-time bus data for the last n minutes (default: 5 minutes):**
   GET /realtime_query?last_min=5
4. **Get all routes:**
   GET /routes
5. **Get all stops:**
   GET /stops
6. **Get all stop times:**
   GET /stop_times
7. **Get all trips:**
   GET /trips
8. Get stops on a specific route (use route_id as a parameter):
   GET /stops_on_route?route_id=142

### Project Structure

- **app.py**: Main application setup and configuration.
- **Model.py**: Defines the database models for GTFS and real-time data.
- **Routes.py**: Contains all the API route definitions and the data fetching logic.
- **run.py**: Entry point to run the Flask application.
- **templates/**: Directory containing HTML templates (if any).

### Notes

- Real-time data is fetched every 10 seconds by default when the `/insert_data?action=start` endpoint is triggered.
- The application uses SQLite for simplicity, but you can switch to another database by changing the configuration in `app.py`.
