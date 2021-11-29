from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

#################################################
# Database Setup
#################################################
# Reference: https://stackoverflow.com/questions/33055039/using-sqlalchemy-scoped-session-in-theading-thread
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)

# Reflect Existing Database Into a New Model
Base = automap_base()
# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home Route - List all routes that are available.
@app.route("/")
def home():
        return (
        f"List All Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"

        )
#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
  #Convert the query results to a dictionary using date as the key and prcp as the value.

  # Calculate the Date 1 Year Ago from the Last Data Point in the Database
  one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
  # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
  prec_data = session.query(Measurement.date, Measurement.prcp).\
  filter(Measurement.date >= one_year_ago).\
  order_by(Measurement.date).all()
  
  prec_data_result = dict(prec_data)
   
  #Return the JSON representation of your dictionary.
  return jsonify(prec_data_result)

#Station Route
@app.route("/api/v1.0/stations")
def stations():
  #Return a JSON list of stations from the dataset.
  stations_all = session.query(Station.station, Station.name).all()
  # Convert List of Tuples Into Normal List
  station_list = list(stations_all)
  # Return JSON List of Stations from the Dataset
  return jsonify(station_list)

#Tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
  #Query the dates and temperature observations of the most active station for the last year of data.
  #Return a JSON list of temperature observations (TOBS) for the previous year.

  # Calculate the Date 1 Year Ago from the Last Data Point in the Database
  one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

  #Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
    
  tobs_list = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
  
  # Convert List of Tuples Into Normal List  
  tobs_result = list(tobs_list)
  
  # Return JSON List of Temperature Observations (tobs) for the Previous Year  
  return jsonify(tobs_result)

#Start Day route
@app.route("/api/v1.0/<start>")
def Start(start):
  #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
   
  start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    group_by(Measurement.date).all()

  # Convert List of Tuples Into Normal List
  start_day_result = list(start_date)
  # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
  return jsonify(start_day_result)



# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
  #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

  start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
  # Convert List of Tuples Into Normal List
  start_end_day_result = list(start_end_day)
  # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
  return jsonify(start_end_day_result)


if __name__ == '__main__':
    app.run(debug=True)



