from flask import render_template, request, url_for, redirect
from DB_Models import Chronometer, Glider, AirplaneFlight,Airplane,User
from __init__ import app,db
from ValidatorClass import *
import datetime

app.secret_key = "Secret Key"


models_dictionary = {
    'Glider': Glider,
    'Airplane': Airplane,
    'User': User
}


@app.route("/", methods=["GET", "POST"])
def main_page():
    """
    Main endpoint displaying two tables with buttons to operate.
    Rozpocznij - if you mark only one check box on lower table and
                    click this button timecount will start and flight record will
                    appear at active flights (upper one) panel.
    Zakoncz - if you mark only one checkbox on higher table and click this button
                 timecount will stop and row will disappear from active flights
                 panel. Difference between starting time and landing time will
                 be saved in database table and be displayed on lower panel.
    Dodaj - button responsible for showing menu responsible for adding
                new record to Chronometer table. You can pick pilot or passenger
                optionally instructor, glider ,airplane , type of start
                tow pilot or winch operator
    Usun - if you mark only one checkbox at bottom table and click this button
                given record will disappear

    GET METHOD - Displays table
    POST METHOD - Reserved for adding another record to the table
    :return:
    """
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
            validator = Validator(flight)
            if validator.validate_chrono_table():
                db.session.add(flight)
                db.session.commit()
            else:
                db.session.rollback()
    chrono = Chronometer.query.all()
    airplanes = Airplane.query.all()
    gliders = Glider.query.all()
    users = User.query.all()
    airplane_flights = AirplaneFlight.query.all()
    return render_template(
        "main.html", chrono=chrono, airplanes=airplanes, gliders=gliders, users=users, airplane_flights=airplane_flights
    )


@app.route("/startflight", methods=["GET", "POST"])
def start_flight():
    """
    Endpoint once again validating Chronometer table record and if everything
    is properly set it sets 'active' parameter to True
    Optionally if start type is Tow launch it creates record in AirplaneFlight
    table - its caused because simple fact of difference between airplane landing
    time and glider landing time in each flight ( they cannot be in same table )
    :return:
    """
    if request.method == 'GET':
        return redirect(url_for(main_page))
    if len(request.form) == 1:
        id = next(iter(request.form))
        flight = Chronometer.query.filter(Chronometer.flight_nr == int(id)).first()
        validator = Validator(flight)
        if validator.validate_chrono_table():
            flight.time_of_start = str(datetime.datetime.now())[11:16]
            if flight.airplane:
                airplane_flight = chrono_to_airplane(flight)
                db.session.add(airplane_flight)
            flight.active = True
            db.session.commit()
    return redirect(url_for("main_page"))


@app.route("/stopflight", methods=["GET", "POST"])
def stop_flight():
    """
    Function which calculates time difference from time of start , put it inside
    datatable and changes record 'active' field for False
    :return:
    """
    if request.method == 'GET':
        return redirect(url_for(main_page))
    if len(request.form) == 1:
        id = next(iter(request.form))
        main_flight = Chronometer.query.filter(
            Chronometer.flight_nr == int(id[1:])).first()
        timedif = time_difference(main_flight.time_of_start,
                                  str(datetime.datetime.now())[11:16])
        if id.startswith("g"):
            main_flight.glider_landing_time = str(datetime.datetime.now())[11:16]
            main_flight.glider_tia = timedif
            main_flight.active = False
            main_flight.glider.time_in_air += int(timedif.split(':')[0]) * 60 + int(timedif.split(':')[1])
            db.session.commit()
        elif id.startswith("a"):
            airplane_flight = AirplaneFlight.query.filter(
                AirplaneFlight.flight_nr == int(id[1:])
            ).first()
            main_flight.airplane_landing_time = str(datetime.datetime.now())[
                                                11:16]
            main_flight.airplane_tia=timedif
            airplane = Airplane.query.filter(Airplane.name == airplane_flight.airplane).first()
            airplane.time_in_air += int(timedif.split(':')[0]) * 60 + int(timedif.split(':')[1])

            db.session.delete(airplane_flight)
        db.session.commit()
    return redirect(url_for("main_page"))


@app.route('/deleteflight',methods=['POST','GET'])
def deleteflight():
    """
    Endpoint which user is sent to deleting a flight from lower panel
    :return:
    """
    if request.method == 'GET':
        return redirect(url_for(main_page))
    if len(request.form) == 1:
        id = next(iter(request.form))
        chrono_obj = Chronometer.query.filter(Chronometer.flight_nr == id).first()
        db.session.delete(chrono_obj)
        db.session.commit()
    return redirect(url_for('main_page'))


@app.route('/manage', methods=['GET'])
def manage():
    """
    Manage page when you can modify users permissions , delete and add users airplanes
    and gliders.
    :return:
    """
    airplanes = Airplane.query.all()
    gliders = Glider.query.all()
    users = User.query.all()
    return render_template('manage.html',airplanes=airplanes,gliders=gliders,users = users)


@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method == 'GET':
        return redirect(url_for(main_page))
    table = models_dictionary.get(request.args.get('table'))
    obj = table.query.filter(table.id == request.args.get('id')).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('manage'))


@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'GET':
        return redirect(url_for(main_page))
    arguments = {argument:request.form.get(argument) for argument in request.form}
    flip_booleans(arguments)
    table = models_dictionary.get(request.args.get('table'))
    table.query.filter(table.id == request.form.get('id')).update(arguments)
    db.session.commit()
    return redirect(url_for('manage'))


@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'GET':
        return redirect(url_for(main_page))
    table = models_dictionary.get(request.args.get('table'))
    arguments = {argument:request.form.get(argument) for argument in request.form}
    flip_booleans(arguments)
    db.session.add(table(**arguments))
    db.session.commit()
    return redirect(url_for('manage'))


if __name__ == "__main__":
    app.run(debug=True)
