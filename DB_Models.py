from __init__ import *

if __name__ == '__main__':
    db.create_all()
    glider1 = Glider(name='Puchacz-3351',time_in_air=15)
    glider2 = Glider(name='Junior-3296', time_in_air=15)
    glider3 = Glider(name='Puchacz-3523', time_in_air=15)
    db.session.add(glider1)
    db.session.add(glider2)
    db.session.add(glider3)

    airplane1 = Airplane(name='SP-CAS',time_in_air=15)
    airplane2 = Airplane(name='SP-WBK',time_in_air=15)
    airplane3 = Airplane(name='SP-KBW',time_in_air=15)
    db.session.add(airplane1)
    db.session.add(airplane2)
    db.session.add(airplane3)

    f1 = Chronometer(
                        date = '06/07/2021',
                        time_of_start="-",
                        glider_landing_time="-",
                        airplane_landing_time="-",
                        glider_tia = "-",
                        airplane_tia = "-",
                        start_type='S',
                        winch_pilot = '',
                        airplane_pilot = "M.Lewandowski",
                        pilot_instructor = "M.Cymanski",
                        passenger_student = "-",
                        glider = 'Puchacz-3351',
                        airplane = 'SP-CAS'
        )
    f2= Chronometer(
                        date = '06/07/2021',
                        time_of_start="-",
                        glider_landing_time="-",
                        airplane_landing_time="-",
                        glider_tia = "-",
                        airplane_tia = "-",
                        start_type='W',
                        winch_pilot = 'L.Szaduro',
                        airplane_pilot = '',
                        pilot_instructor = 'R.Manka',
                        passenger_student = 'K.Jaworska',
                        glider = 'Puchacz-3351',
                        airplane = '-'
        )
    f3 = Chronometer(
                        date = '06/07/2021',
                        time_of_start="-",
                        glider_landing_time="-",
                        airplane_landing_time="-",
                        glider_tia = "-",
                        airplane_tia = "-",
                        start_type='S',
                        winch_pilot = '',
                        airplane_pilot = "M.Lewandowski",
                        pilot_instructor = 'R.Berk',
                        passenger_student = 'T.Kowalski',
                        glider = 'Puchacz-3351',
                        airplane = 'SP-CAS'
        )

    a1 = ActiveFlights(
                        date = '06/07/2021',
                        time_of_start="-",
                        glider_landing_time="-",
                        airplane_landing_time="-",
                        glider_tia = "-",
                        airplane_tia = "-",
                        start_type='S',
                        winch_pilot = '',
                        airplane_pilot = "M.Lewandowski",
                        pilot_instructor = "T.Bienkowski",
                        passenger_student = "-",
                        glider = 'Puchacz-3351',
                        airplane = 'SP-CAS'
        )
    a2= ActiveFlights(
                        date = '06/07/2021',
                        time_of_start="-",
                        glider_landing_time="-",
                        airplane_landing_time="-",
                        glider_tia = "-",
                        airplane_tia = "-",
                        start_type='W',
                        winch_pilot = 'L.Szaduro',
                        airplane_pilot = '',
                        pilot_instructor = 'T.Zbucki',
                        passenger_student = '-',
                        glider = 'Puchacz-3351',
                        airplane = '-'
        )
    a3 = ActiveFlights(
                        date = '06/07/2021',
                        time_of_start="-",
                        glider_landing_time="-",
                        airplane_landing_time="-",
                        glider_tia = "-",
                        airplane_tia = "-",
                        start_type='S',
                        winch_pilot = '',
                        airplane_pilot = "M.Lewandowski",
                        pilot_instructor = 'W.Tomczynski',
                        passenger_student = '-',
                        glider = 'Puchacz-3351',
                        airplane = 'SP-CAS'
        )

    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column('firstname',db.String(25),nullable=False)
    lastname = db.Column('lastname',db.String(25),nullable=False)
    member = db.Column('member',db.Boolean)

    p1 = Pilot(firstname='Roman',lastname='Berk',member=1)
    p2 = Pilot(firstname='Ryszard',lastname='Manka',member=1)
    p3 = Pilot(firstname='Jacek',lastname='Sobolewski',member=1)

    ap1 = AirplanePilot(firstname='Maksymilian',lastname='Lewandowski',member=1)
    ap2 = AirplanePilot(firstname='Jacek',lastname='Sobolewski',member=1)
    ap3 = AirplanePilot(firstname='Sebastian',lastname='Jabłonski',member=1)

    wo1 = WinchOperator(firstname='Jacek',lastname='Sobolewski',launches=5)
    wo2 = WinchOperator(firstname='Roman',lastname='Berk',launches=4)
    wo3 = WinchOperator(firstname='Lech',lastname='Szaduro',launches=3)

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)

    db.session.add(wo1)
    db.session.add(wo2)
    db.session.add(wo3)

    db.session.add(ap1)
    db.session.add(ap2)
    db.session.add(ap3)

    db.session.add(f1)
    db.session.add(f2)
    db.session.add(f3)
    # db.session.add(a1)
    # db.session.add(a2)
    # db.session.add(a3)

    db.session.commit()
    db.session.close()
    print("ok")

