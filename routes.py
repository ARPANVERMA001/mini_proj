from flask import render_template, request
from Model import Routes, Stops

def register_routes(app, db):

    @app.route('/')
    def index():
        r = Routes.query.all()
        return str(r)
    