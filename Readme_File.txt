Readme File:

Run the run.py file to start the app.

The following endpoints are used:

[1]
Start to insert the realtime data into db:
http://localhost:5000/insert_data?action=start

[2]
Stop the insertion of realtime data into db:
http://localhost:5000/insert_data?action=stop

[3]
Gets the data of buses stored in db till last_min:
http://localhost:5000/realtime_query?last_min=5

[4]
Gets the Routes data:
http://localhost:5000/routes

[5]
Gets the Stops data:
http://localhost:5000/stops

[6]
Gets the Stop_times data:
http://localhost:5000/stop_times

[7]
Gets the Trips data:
http://localhost:5000/trips

[8]
Gets the Stops on route_id data:
Here route_id is an argument, change it accordingly.
http://localhost:5000/stops_on_route?route_id=142