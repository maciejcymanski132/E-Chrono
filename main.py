from flask import render_template, request, url_for, redirect
from __init__ import Chronometer, Glider, db, ActiveFlights, AirplaneFlight,Airplane,Pilot,AirplanePilot,WinchOperator,app,User
from jinja2 import Template
import datetime

app.secret_key = "Secret Key"

myrandomdict = {
    'Pilot': Pilot,
    'AirplanePilot': AirplanePilot,
    'Glider': Glider,
    'Airplane': Airplane,
    'WinchOperator': WinchOperator,
    'User':User
}

def chrono_to_active(chrono_object):
    return ActiveFlights(
        date="06/07/2021",
        flight_nr=chrono_object.flight_nr,
        time_of_start=chrono_object.time_of_start,
        glider_landing_time=chrono_object.glider_landing_time,
        airplane_landing_time=chrono_object.airplane_landing_time,
        glider_tia=chrono_object.glider_tia,
        airplane_tia=chrono_object.airplane_tia,
        start_type=chrono_object.start_type,
        winch_pilot=chrono_object.winch_pilot,
        airplane_pilot=chrono_object.airplane_pilot,
        instructor=chrono_object.instructor,
        pilot_passenger=chrono_object.pilot_passenger,
        glider=chrono_object.glider,
        airplane=chrono_object.airplane,
    )


def active_to_chrono(active_object):
    return Chronometer(
        date="06/07/2021",
        flight_nr=active_object.flight_nr,
        time_of_start=active_object.time_of_start,
        glider_landing_time=active_object.glider_landing_time,
        airplane_landing_time=active_object.airplane_landing_time,
        glider_tia=active_object.glider_tia,
        airplane_tia=active_object.airplane_tia,
        start_type=active_object.start_type,
        winch_pilot=active_object.winch_pilot,
        airplane_pilot=active_object.airplane_pilot,
        instructor=active_object.instructor,
        pilot_passenger=active_object.pilot_passenger,
        glider=active_object.glider,
        airplane=active_object.airplane,
    )


def flip_booleans(arguments):
    for key,value in arguments.items():
        if value == 'true':
            arguments[key] = True
        if value == 'false':
            arguments[key] = False


def aircrafts_taken(flight):
    airplanes_taken = [
        i[0] for i in AirplaneFlight.query.with_entities(AirplaneFlight.airplane).all()
    ]
    gliders_taken = [
        i[0] for i in ActiveFlights.query.with_entities(ActiveFlights.glider).all()
    ]
    if flight.glider not in gliders_taken and flight.airplane not in airplanes_taken:
        return False
    return True


def validate_start_type(flight):
    if (flight.airplane == '-' and flight.start_type == 'W') or \
    (flight.airplane != '-' and flight.start_type == 'S'):
        return True
    return False


def validate_flight(flight):
    active_ids = [
        id[0] for id in ActiveFlights.query.with_entities(ActiveFlights.flight_nr).all()
    ]
    if (
        flight.flight_nr not in active_ids
        and flight.time_of_start == "-"
        and not aircrafts_taken(flight)
    ):
        return True


def validate_operators(active_obj):
    if active_obj.airplane_pilot == '-' and active_obj.winch_pilot == '-'\
            or active_obj.airplane_pilot != '-' and active_obj.winch_pilot != '-':
        return False
    return True


def time_difference(time1, time2):
    t1 = datetime.datetime.strptime(time1, "%H:%M")
    t2 = datetime.datetime.strptime(time2, "%H:%M")
    return str(t2 - t1)[0:4]


def active_to_airplane(active_object):
    return AirplaneFlight(
        date="06/07/2021",
        flight_nr=active_object.flight_nr,
        time_of_start=active_object.time_of_start,
        airplane_landing_time=active_object.airplane_landing_time,
        airplane_tia=active_object.airplane_tia,
        airplane_pilot=active_object.airplane_pilot,
        airplane=active_object.airplane,
    )


@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == 'POST':
        if len(request.form) == 7:
            r = request.form
            o = Chronometer(date='12/06/2021',
                            instructor = r.get('instructor'),
                            pilot_passenger = r.get('pilot_passenger'),
                            time_of_start = '-',
                            glider_landing_time='-',
                            airplane_landing_time='-',
                            glider_tia = '-',
                            airplane_tia = '-',
                            start_type = r.get('start_type'),
                            winch_pilot = r.get('winch_pilot'),
                            airplane_pilot = r.get('airplane_pilot'),
                            glider = r.get('glider'),
                            airplane = r.get('airplane'))

            if validate_start_type(o) and validate_operators(o) and\
                    (r.get('winch_pilot') == '-' or r.get('airplane_pilot') == '-'):
                db.session.add(o)
                db.session.commit()
    chrono = Chronometer.query.all()
    active = ActiveFlights.query.all()
    airplane = AirplaneFlight.query.all()
    airplanes = Airplane.query.all()
    gliders = Glider.query.all()
    users = User.query.all()
    return render_template(
        "main.html", active_flights=active, chrono=chrono,
        airplane_flights=airplane,airplanes=airplanes,gliders=gliders,users = users
    )


@app.route("/startflight", methods=["GET", "POST"])
def start_flight():
    if len(request.form) == 1:
        id = next(iter(request.form))
        flight = Chronometer.query.filter(Chronometer.flight_nr == int(id)).first()
        if validate_flight(flight):
            active_obj = chrono_to_active(flight)
            active_obj.time_of_start = str(datetime.datetime.now())[11:16]
            if validate_operators(active_obj):
                if active_obj.airplane != '-':
                    airplane_flight = active_to_airplane(active_obj)
                    db.session.add(airplane_flight)
                if active_obj.winch_pilot != '-':
                    for operator in WinchOperator.query.all():
                        if active_obj.winch_pilot == f'{operator.firstname} {operator.lastname}':
                            winch_operator = operator
                            winch_operator.launches = winch_operator.launches + 1
                db.session.add(active_obj)
            db.session.commit()
    return redirect(url_for("main_page"))


@app.route("/stopflight", methods=["GET", "POST"])
def stop_flight():
    if len(request.form) == 1:
        id = next(iter(request.form))
        if id.startswith("g"):
            active_flight = ActiveFlights.query.filter(
                ActiveFlights.flight_nr == int(id[1:])).first()
            timedif = time_difference(active_flight.time_of_start,
                                      str(datetime.datetime.now())[11:16])
            Chronometer.query.filter(
                Chronometer.flight_nr == active_flight.flight_nr
            ).update(
                dict(
                    time_of_start=active_flight.time_of_start,
                    glider_landing_time=str(datetime.datetime.now())[11:16],
                    glider_tia=timedif,
                )
            )
            glider = Glider.query.filter(Glider.name == active_flight.glider).first()

            glider.time_in_air += int(timedif.split(':')[0]) * 60 + int(timedif.split(':')[1])
            db.session.delete(active_flight)
            db.session.commit()

        elif id.startswith("a"):
            airplane_obj = AirplaneFlight.query.filter(
                AirplaneFlight.flight_nr == int(id[1:])
            ).first()
            timedif = time_difference(
                        airplane_obj.time_of_start,
                        str(datetime.datetime.now())[11:16])
            Chronometer.query.filter(
                Chronometer.flight_nr == int(id[1:])
            ).update(
                dict(
                    time_of_start=airplane_obj.time_of_start,
                    airplane_landing_time=str(datetime.datetime.now())[11:16],
                    airplane_tia = timedif
                    )
                )
            airplane = Airplane.query.filter(Airplane.name == airplane_obj.airplane).first()
            airplane.time_in_air += int(timedif.split(':')[0]) * 60 + int(timedif.split(':')[1])
            db.session.delete(airplane_obj)
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
    pilots = Pilot.query.all()
    airplanepilots = AirplanePilot.query.all()
    winchoperators = WinchOperator.query.all()
    users = User.query.all()
    return render_template('manage.html',airplanes=airplanes,gliders=gliders,pilots=pilots,
        airplanepilots = airplanepilots, winchoperators = winchoperators,users = users)


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
    print(table.query.filter(table.id == request.form.get('id')).all(),arguments)
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
