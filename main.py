from flask import render_template, request, url_for, redirect
from __init__ import Chronometer, Glider, db, AirplaneFlight,Airplane,app,User
from jinja2 import Template
import datetime

app.secret_key = "Secret Key"


myrandomdict = {
    'Glider': Glider,
    'Airplane': Airplane,
    'User':User
}


def check_if_aircrafts_taken(flight):
    active_flights = Chronometer.query.filter(Chronometer.active == True).all()
    for af in active_flights:
        if af.airplane.id == flight.airplane.id or af.glider.id == flight.glider.id:
            return True
    return False


def check_users_permissions(flight):
    if flight.instructor:
        if not flight.instructor.instructor:
            return False
    if flight.pilot_passenger.id != 0:
        if not flight.pilot_passenger.glider_pilot:
            return False
    if flight.pilot_passenger.id == 0:
        if not flight.instructor:
            print('nodziala')
            return False
    if flight.winch_operator:
        if not flight.winch_operator.winch_operator:
            return False
    if flight.tow_pilot:
        if not flight.tow_pilot.airplane_pilot:
            return False
    return True

def check_start_type(flight):
    if flight.start_type == 'W' and flight.tow_pilot:
        return False
    if flight.start_type == 'S' and flight.winch_operator:
        return False
    if flight.start_type == 'S' and not flight.airplane:
        return False
    return True

def validate_operators(flight):
    if (flight.tow_pilot and flight.winch_operator) or (not flight.tow_pilot and not flight.winch_operator):
        return False
    return True

def validate_chrono_table(flight):
    if check_if_aircrafts_taken(flight):
        return False
    if not check_users_permissions(flight):
        return False
    if not check_start_type(flight):
        return False
    if not validate_operators(flight):
        return False
    return True


def flip_booleans(arguments):
    for key,value in arguments.items():
        if value == 'true':
            arguments[key] = True
        if value == 'false':
            arguments[key] = False


def validate_flight(flight):
    active_flights = [f[0] for f in Chronometer.query.\
        filter(Chronometer.active == True).with_entities(Chronometer.flight_nr).all()]
    if flight.flight_nr not in active_flights\
        and flight.time_of_start == "-"\
        and not check_if_aircrafts_taken(flight):
        return True


def time_difference(time1, time2):
    t1 = datetime.datetime.strptime(time1, "%H:%M")
    t2 = datetime.datetime.strptime(time2, "%H:%M")
    return str(t2 - t1)[0:4]


def chrono_to_airplane(chrono_object):
    return AirplaneFlight(
        flight_nr=chrono_object.flight_nr,
        time_of_start=chrono_object.time_of_start,
        airplane_pilot=chrono_object.tow_pilot.id,
        airplane=Airplane.query.filter(Airplane.id == chrono_object.airplane.id).first().name,
    )


@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == 'POST':
        if len(request.form) == 7:
            r = request.form
            flight = Chronometer(
                            instructor=User.query.filter(User.id == r.get('instructor')).first(),
                            pilot_passenger=User.query.filter(User.id == r.get('pilot_passenger')).first(),
                            start_type=r.get('start_type'),
                            winch_operator=User.query.filter(User.id == r.get('winch_pilot')).first(),
                            tow_pilot=User.query.filter(User.id == r.get('airplane_pilot')).first(),
                            glider=Glider.query.filter(Glider.id == r.get('glider')).first(),
                            airplane=Airplane.query.filter(Airplane.id == r.get('airplane')).first()
                            )

            if validate_chrono_table(flight):
                db.session.add(flight)
                db.session.commit()
            else:
                db.session.delete(flight)
    chrono = Chronometer.query.all()
    airplanes = Airplane.query.all()
    gliders = Glider.query.all()
    users = User.query.all()
    airplane_flights = AirplaneFlight.query.all()
    return render_template(
        "main.html", chrono=chrono,airplanes=airplanes,gliders=gliders,users = users,airplane_flights=airplane_flights
    )


@app.route("/startflight", methods=["GET", "POST"])
def start_flight():
    if len(request.form) == 1:
        id = next(iter(request.form))
        flight = Chronometer.query.filter(Chronometer.flight_nr == int(id)).first()
        if validate_flight(flight):
            flight.time_of_start = str(datetime.datetime.now())[11:16]
            if validate_operators(flight):
                if flight.airplane:
                    airplane_flight = chrono_to_airplane(flight)
                    db.session.add(airplane_flight)
                flight.active = True
            db.session.commit()
    return redirect(url_for("main_page"))


@app.route("/stopflight", methods=["GET", "POST"])
def stop_flight():
    if len(request.form) == 1:
        id = next(iter(request.form))
        main_flight = Chronometer.query.filter(
            Chronometer.flight_nr == int(id[1:])).first()
        timedif = time_difference(main_flight.time_of_start,
                                  str(datetime.datetime.now())[11:16])
        if id.startswith("g"):
            main_flight.glider_landing_time = str(datetime.datetime.now())[11:16]
            main_flight.glider_tia = timedif
            #fix this so time counts by its own in sqltable
            main_flight.glider.time_in_air += int(timedif.split(':')[0]) * 60 + int(timedif.split(':')[1])
            db.session.commit()
        elif id.startswith("a"):
            airplane_flight = AirplaneFlight.query.filter(
                AirplaneFlight.flight_nr == int(id[1:])
            ).first()
            main_flight.airplane_landing_time = str(datetime.datetime.now())[
                                                11:16]
            main_flight.airplane_tia=timedif
            #fix this so time counts by its own in sqltable
            airplane = Airplane.query.filter(Airplane.name == airplane_flight.airplane).first()
            airplane.time_in_air += int(timedif.split(':')[0]) * 60 + int(timedif.split(':')[1])
            db.session.delete(airplane_flight)
        db.session.commit()
    return redirect(url_for("main_page"))


@app.route('/deleteflight',methods=['POST','GET'])
def deleteflight():
    if len(request.form) == 1:
        id = next(iter(request.form))
        chrono_obj = Chronometer.query.filter(Chronometer.flight_nr == id).first()
        db.session.delete(chrono_obj)
        db.session.commit()
    return redirect(url_for('main_page'))


@app.route('/manage',methods=['POST','GET'])
def manage():
    airplanes = Airplane.query.all()
    gliders = Glider.query.all()
    users = User.query.all()
    return render_template('manage.html',airplanes=airplanes,gliders=gliders,users = users)


@app.route('/delete',methods=['GET','POST'])
def delete():
    table = myrandomdict.get(request.args.get('table'))
    obj = table.query.filter(table.id == request.args.get('id')).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('manage'))


@app.route('/update',methods=['GET','POST'])
def update():
    arguments = {argument:request.form.get(argument) for argument in request.form}
    flip_booleans(arguments)
    table = myrandomdict.get(request.args.get('table'))
    table.query.filter(table.id == request.form.get('id')).update(arguments)
    db.session.commit()
    return redirect(url_for('manage'))


@app.route('/add',methods=['GET','POST'])
def add():
    table = myrandomdict.get(request.args.get('table'))
    arguments = {argument:request.form.get(argument) for argument in request.form}
    flip_booleans(arguments)
    db.session.add(table(**arguments))
    db.session.commit()
    return redirect(url_for('manage'))


if __name__ == "__main__":
    app.run(debug=True)
