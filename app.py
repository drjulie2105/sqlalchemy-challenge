import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/prescipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    prcp_date = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        prcp_date_list.append(new_dict)

    session.close()

    return jsonify(prcp_date)

    session.close()


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name).all()

    station_list=[]

    for station, name in results:
        station[station]=name

    session.close()
    
    return jsonify (station_list)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Get the last date contained in the dataset and date from one year ago
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year_date = (dt.datetime.strptime(last_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    # Query for the dates and temperature values
    results =   session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= last_year_date).\
                order_by(Measurement.date).all()

    # Convert to list of dictionaries to jsonify
    tobs_list = []

    for date, tobs in results:
        new_dict = {}
        new_dict[date] = tobs
        tobs_date_list.append(new_dict)

    session.close()

    return jsonify(tobs_list)




if __name__ == '__main__':
    app.run(debug=True)
