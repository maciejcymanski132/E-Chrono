from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///my_db.db"
db = SQLAlchemy(app)


class Glider(db.Model):
    __tablename__ = 'glider'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(20), nullable=False)
    time_in_air = db.Column('time_in_air', db.Integer,default=0)


class Airplane(db.Model):

    __tablename__ = 'airplane'

    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name',db.String(20), nullable=False)
    time_in_air = db.Column('time_in_air', db.Integer,default=0)

class AirplanePilot(db.Model):

    __tablename__ = 'airplanepilot'
    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column('firstname',db.String(25),nullable=False)
    lastname = db.Column('lastname',db.String(25),nullable=False)

class WinchOperator(db.Model):

    __tablename__ = 'winchoperator'

    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column('firstname',db.String(25),nullable=False)
    lastname = db.Column('lastname',db.String(25),nullable=False)
    launches = db.Column('launches',db.Integer,default=0)


class Pilot(db.Model):

    __tablename__ = 'pilot'

    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column('firstname',db.String(25),nullable=False)
    lastname = db.Column('lastname',db.String(25),nullable=False)

class AirplaneFlight(db.Model):

    __tablename__ = 'airplaneflight'
    date = db.Column('date',db.String(10))
    flight_nr = db.Column('flight_nr',db.Integer,primary_key=True)
    time_of_start = db.Column('time_of_start',db.String(5))
    airplane_landing_time = db.Column('airplane_landing_time',db.String(5))
    airplane_tia = db.Column('airplane_tia',db.String(5))
    airplane_pilot = db.Column('airplane_pilot',db.String(20))
    airplane = db.Column('airplane',db.String(15))


class ActiveFlights(db.Model):

    __tablename__ = 'active_flights'

    date = db.Column('date',db.String(10))
    flight_nr =db.Column('flight_nr',db.Integer, primary_key=True)
    time_of_start = db.Column('time_of_start',db.String(5))
    glider_landing_time = db.Column('glider_landing_time',db.String(5),nullable=False)
    airplane_landing_time = db.Column('airplane_landing_time',db.String(5))
    glider_tia = db.Column('glider_tia',db.String(5),nullable=False)
    airplane_tia = db.Column('airplane_tia', db.String(5))
    start_type = db.Column('start_type', db.String(1))
    winch_pilot = db.Column('winch_pilot', db.String(20))
    airplane_pilot = db.Column('airplane_pilot', db.String(20))
    pilot_instructor = db.Column('pilot_instructor', db.String(15))
    passenger_student = db.Column('passenger_student', db.String(15))
    glider = db.Column('glider', db.String(15))
    airplane = db.Column('airplane', db.String(15))


class Chronometer(db.Model):

    __tablename__ = 'chrono'

    date = db.Column('date', db.String(10))
    flight_nr = db.Column('flight_nr', db.Integer, primary_key=True, autoincrement=True)
    time_of_start = db.Column('time_of_start', db.String(5))
    glider_landing_time = db.Column('glider_landing_time', db.String(5), nullable=False)
    airplane_landing_time = db.Column('airplane_landing_time', db.String(5))
    glider_tia = db.Column('glider_tia', db.String(5), nullable=False)
    airplane_tia = db.Column('airplane_tia', db.String(5))
    start_type = db.Column('start_type', db.String(1))
    winch_pilot = db.Column('winch_pilot', db.String(20))
    airplane_pilot = db.Column('airplane_pilot', db.String(20))
    pilot_instructor = db.Column('pilot_instructor', db.String(15))
    passenger_student = db.Column('passenger_student', db.String(15))
    glider = db.Column('glider', db.String(15),)
    airplane = db.Column('aeroplane', db.String(15))

