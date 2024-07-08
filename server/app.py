# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route("/earthquakes/<int:id>")
def get_by_id(id):
    quake = Earthquake.query.filter_by(id = id).first()
    if quake:
        quake_dict = {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
      }
        status = 200
    else:
        quake_dict = {
            "message": f"Earthquake {id} not found."
        }
        status = 404
    return make_response(quake_dict, status)

@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_by_magnitude(magnitude):
    mag = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    mag_dict = {
        "count": len(mag),
        "quakes": [
            {
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year
            }
            for earthquake in mag
        ]
    }
    response_code = 200
    return make_response(mag_dict, response_code)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
