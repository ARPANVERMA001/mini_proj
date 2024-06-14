# The queries for test.db
from app import create_app, db
from Model import Routes, Stops, Trips, StopTimes, RealtimeBus

temp_test_instance = create_app()

with temp_test_instance.app_context():
    
    

    # rout = Routes.query.all()
    # print(rout[:10])

    # stp = Stops.query.all()
    # print(stp[:10])

    # stp_tms = StopTimes.query.all()
    # print(stp_tms[:10])

    # trps = Trips.query.all()
    # print(trps[:10])

    # route_id = 142

    # stops_on_route = (
    #     db.session.query(Stops)
    #     .join(StopTimes, Stops.stop_id == StopTimes.stop_id)
    #     .join(Trips, StopTimes.trip_id == Trips.trip_id)
    #     .join(Routes, Trips.route_id == Routes.route_id)
    #     .filter(Routes.route_id == route_id)
    #     .order_by(StopTimes.stop_sequence)
    #     .all()
    # )
    
    # for stop in stops_on_route:
    #     # print(f"Stop ID: {stop.stop_id}, Stop Name: {stop.stop_name}, Stop Lat: {stop.stop_lat}, Stop Lon: {stop.stop_lon}")
    #     print(f"{stop.stop_id}")