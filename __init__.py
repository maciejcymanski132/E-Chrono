from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_db.db"
db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = "user"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column("firstname", db.String(25), nullable=False)
    lastname = db.Column("lastname", db.String(25), nullable=False)
    instructor = db.Column("instructor", db.Boolean, default=False)
    winch_operator = db.Column("winch_operator", db.Boolean, default=False)
    glider_pilot = db.Column("glider_pilot", db.Boolean, default=False)
    airplane_pilot = db.Column("airplane_pilot", db.Boolean, default=False)

    tow_pulls = db.relationship(
        "Chronometer",
        backref="tow_pilot",
        lazy="dynamic",
        foreign_keys="Chronometer.tow_pilot_id",
    )
    winch_pulls = db.relationship(
        "Chronometer",
        backref="winch_operator",
        lazy="dynamic",
        foreign_keys="Chronometer.winch_operator_id",
    )
    instructor_flights = db.relationship(
        "Chronometer",
        backref="instructor",
        lazy="dynamic",
        foreign_keys="Chronometer.instructor_id",
    )
    flights = db.relationship(
        "Chronometer",
        backref="pilot_passenger",
        lazy="dynamic",
        foreign_keys="Chronometer.pilot_passenger_id",
    )


time_of_start = '-',
glider_landing_time = '-',
airplane_landing_time = '-',
glider_tia = '-',
airplane_tia = '-',

class Chronometer(db.Model):

    __tablename__ = "chrono"

    flight_nr = db.Column("flight_nr", db.Integer, primary_key=True, autoincrement=True)
    time_of_start = db.Column("time_of_start", db.String(5),default='-')
    glider_landing_time = db.Column("glider_landing_time", db.String(5), nullable=False,default='-')
    airplane_landing_time = db.Column("airplane_landing_time", db.String(5),default='-')
    glider_tia = db.Column("glider_tia", db.String(5), nullable=False,default='-')
    airplane_tia = db.Column("airplane_tia", db.String(5),default='-')
    start_type = db.Column("start_type", db.String(1))

    winch_operator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tow_pilot_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    instructor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pilot_passenger_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    glider_id = db.Column(db.Integer, db.ForeignKey("glider.id"))
    airplane_id = db.Column(db.Integer, db.ForeignKey("airplane.id"))

    active = db.Column('active',db.Boolean,default=False)


class Glider(db.Model):
    __tablename__ = "glider"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(20), nullable=False)
    time_in_air = db.Column("time_in_air", db.Integer, default=0)

    flights = db.relationship("Chronometer", backref="glider")


class Airplane(db.Model):

    __tablename__ = "airplane"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(20), nullable=False)
    time_in_air = db.Column("time_in_air", db.Integer, default=0)

    flights = db.relationship("Chronometer", backref="airplane")


class AirplaneFlight(db.Model):

    __tablename__ = "airplaneflight"
    flight_nr = db.Column("flight_nr", db.Integer, primary_key=True)
    time_of_start = db.Column("time_of_start", db.String(5))
    airplane_pilot = db.Column("airplane_pilot", db.Integer)
    airplane = db.Column("airplane", db.String(15))
