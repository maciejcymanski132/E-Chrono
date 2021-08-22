from flask import render_template, request, url_for, redirect, Flask , flash
from __init__ import app, db
from __init__ import Chronometer, Glider, db, ActiveFlights, AirplaneFlight,Airplane
from jinja2 import Template
import datetime

app.secret_key = "Secret Key"

def refresh_tables(app_obj):
    chrono_table = Template(
        """<table id="chronotable">
                <tr class="nothover">
                    <th></th>
                    <th>Pilot/Instruktor</th>
                    <th>Pasazer/Uczen</th>
                    <th>Szybowiec</th>
                    <th>S.Holujacy</th>
                    <th>Czas Startu</th>
                    <th>Czas ladowania(SZ)</th>
                    <th>Czas ladowania(S)</th>
                    <th>Czas w powietrzu(SZ)</th>
                    <th>Czas w powietrzu(S)</th>
                    <th>Rodzaj startu</th>
                    <th>Wyciagarkowy/Pilot</th>
                </tr>
                {% for c in chrono %}
                <tr>
                    <td><input type="checkbox" name={{c.flight_nr}}></td>
                    <td>{{c.pilot_instructor}}</td>
                    <td>{{c.passenger_student}}</td>
                    <td>{{c.glider}}</td>
                    <td>{{c.airplane}}</td>
                    <td>{{c.time_of_start}}</td>
                    <td>{{c.glider_landing_time}}</td>
                    <td>{{c.airplane_landing_time}}</td>
                    <td>{{c.glider_tia}}</td>
                    <td>{{c.airplane_tia}}</td>
                    <td>{{c.start_type}}</td>
                    <td>{{c.winch_pilot}}</td>
                </tr>
                {% endfor %}
            </table>"""
    )

    chrono_table = chrono_table.render(chrono=Chronometer.query.all())
    app_obj.js.document.getElementById("chronotable").innerHTML = chrono_table
    active_table = Template(
        """
    <table id="activetable">
            <tr class="nothover">
                <th></th>
                <th>Pilot/Instruktor</th>
                <th>Pasazer/Uczen</th>
                <th>Szybowiec</th>
                <th>Czas Startu</th>
                <th>Czas ladowania(SZ)</th>
                <th>Czas ladowania(S)</th>
            </tr>
            {% for a in active_flights %}
            <tr>
                <td><input type="checkbox" name={{a.flight_nr}}></td>
                <td>{{a.pilot_instructor}}</td>
                <td>{{a.passenger_student}}</td>
                <td>{{a.glider}}</td>
                <td>{{a.time_of_start}}</td>
                <td>{{a.glider_landing_time}}</td>
                <td>{{a.airplane_landing_time}}</td>
            </tr>
            {% endfor %}
        </table>"""
    )
    active_table = active_table.render(active_flights=ActiveFlights.query.all())
    app_obj.js.document.getElementById("activetable").innerHTML = active_table


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
        pilot_instructor=chrono_object.pilot_instructor,
        passenger_student=chrono_object.passenger_student,
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
        pilot_instructor=active_object.pilot_instructor,
        passenger_student=active_object.passenger_student,
        glider=active_object.glider,
        airplane=active_object.airplane,
    )

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

def validate_active(active_obj):
    print(active_obj.airplane_pilot,active_obj.winch_pilot)
    if active_obj.airplane_pilot == '' and active_obj.winch_pilot == ''\
            or active_obj.airplane_pilot != '' and active_obj.winch_pilot != '':
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
def print_hi():
    if request.method == 'POST':
        if len(request.form) == 7:
            r = request.form
            o = Chronometer(date='12/06/2021',
                            pilot_instructor = r.get('pilot_instructor'),
                            passenger_student = r.get('passenger_student'),
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
            print('almost')
            if validate_start_type(o):
                db.session.add(o)
                db.session.commit()
    chrono = Chronometer.query.all()
    active = ActiveFlights.query.all()
    airplane = AirplaneFlight.query.all()
    airplanes = Airplane.query.all()
    gliders = Glider.query.all()
    return render_template(
        "main.html", active_flights=active, chrono=chrono,
        airplane_flights=airplane,airplanes=airplanes,gliders=gliders
    )


@app.route("/startflight", methods=["GET", "POST"])
def start_flight():
    if len(request.form) == 1:
        id = next(iter(request.form))
        flight = Chronometer.query.filter(Chronometer.flight_nr == int(id)).first()
        if validate_flight(flight):
            print('uno')
            active_obj = chrono_to_active(flight)
            active_obj.time_of_start = str(datetime.datetime.now())[11:16]
            if validate_active(active_obj):
                print('dos')
                print(active_obj.airplane)
                if active_obj.airplane != '-':
                    print('tres')
                    airplane_flight = active_to_airplane(active_obj)
                    db.session.add(airplane_flight)
                db.session.add(active_obj)
            db.session.commit()
    return redirect(url_for("print_hi"))


@app.route("/stopflight", methods=["GET", "POST"])
def stop_flight():
    if len(request.form) == 1:
        id = next(iter(request.form))
        if id.startswith("g"):
            active_flight = ActiveFlights.query.filter(
                ActiveFlights.flight_nr == int(id[1:])).first()
            Chronometer.query.filter(
                Chronometer.flight_nr == active_flight.flight_nr
            ).update(
                dict(
                    time_of_start=active_flight.time_of_start,
                    glider_landing_time=str(datetime.datetime.now())[11:16],
                    glider_tia=time_difference(
                                            active_flight.time_of_start,
                                            str(datetime.datetime.now())[11:16]),
                )
            )
            db.session.delete(active_flight)

        if id.startswith("a"):
            airplane_obj = AirplaneFlight.query.filter(
                AirplaneFlight.flight_nr == int(id[1:])
            ).first()
            Chronometer.query.filter(
                Chronometer.flight_nr == int(id[1:])
            ).update(
                dict(
                    time_of_start=airplane_obj.time_of_start,
                    airplane_landing_time=str(datetime.datetime.now())[11:16],
                    airplane_tia = time_difference(
                        airplane_obj.time_of_start,
                        str(datetime.datetime.now())[11:16])
                    )
                )
            db.session.delete(airplane_obj)
        db.session.commit()
    return redirect(url_for("print_hi"))

@app.route('/updateflight',methods=['GET','POST'])
def updateflight():
    if request.method == 'POST':
        my_data = Chronometer.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
@app.route('/deleteflight',methods=['POST','GET'])
def deleteflight():
    if len(request.form) == 1:
        id = next(iter(request.form))
        chrono_obj = Chronometer.query.filter(Chronometer.flight_nr == id).first()
        db.session.delete(chrono_obj)
        db.session.commit()
    return redirect(url_for('print_hi'))

if __name__ == "__main__":
    app.run(debug=True)
