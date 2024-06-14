from flask import Flask, jsonify
from app import create_app, db
from Model import RealtimeBus  # Import the RealtimeBus model
from datetime import datetime, timedelta
from dateutil import parser

app = create_app()

with app.app_context():
    def get_realtime_data_route(last_min=1):
        now = datetime.now()
        print(f"Now: {now}")
        delta = now - timedelta(minutes=last_min)
        print(f"Delta: {delta}")

        # Corrected filter using vehicle_datetime attribute
        realtime_data = RealtimeBus.query.filter(
            RealtimeBus.vehicle_datetime >= delta, RealtimeBus.vehicle_datetime <= now
        ).all()

        # print(f"Realtime Data: {realtime_data}")
        return jsonify([data.to_dict() for data in realtime_data])
    
    ans=get_realtime_data_route()
    print(ans.json)