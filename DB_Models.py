from __init__ import *

if __name__ == '__main__':
    db.create_all()
    glider1 = Glider(name='Puchacz-3351')
    glider2 = Glider(name='Junior-3296')
    glider3 = Glider(name='Puchacz-3523')
    db.session.add(glider1)
    db.session.add(glider2)
    db.session.add(glider3)

    airplane1 = Airplane(name='SP-CAS')
    airplane2 = Airplane(name='SP-WBK')
    airplane3 = Airplane(name='SP-KBW')
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
                        winch_pilot = '-',
                        airplane_pilot = "M.Lewandowski",
                        instructor = "M.Cymanski",
                        pilot_passenger = "-",
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
                        airplane_pilot = '-',
                        instructor = 'R.Manka',
                        pilot_passenger = 'K.Jaworska',
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
                        winch_pilot = '-',
                        airplane_pilot = "M.Lewandowski",
                        instructor = 'R.Berk',
                        pilot_passenger = 'T.Kowalski',
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
                        instructor = "T.Bienkowski",
                        pilot_passenger = "-",
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
                        instructor = 'T.Zbucki',
                        pilot_passenger = '-',
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
                        instructor = 'W.Tomczynski',
                        pilot_passenger = '-',
                        glider = 'Puchacz-3351',
                        airplane = 'SP-CAS'
        )

    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column('firstname',db.String(25),nullable=False)
    lastname = db.Column('lastname',db.String(25),nullable=False)

    p1 = Pilot(firstname='Roman',lastname='Berk',instructor=True)
    p2 = Pilot(firstname='Ryszard',lastname='Manka',instructor=True)
    p3 = Pilot(firstname='Jacek',lastname='Sobolewski',instructor=True)
    p4 = Pilot(firstname='Maciej',lastname='Cymanski')
    p5 = Pilot(firstname='Mikołaj',lastname='Szyszka')

    u1 = User(firstname='Roman',lastname='Berk',instructor=True,winch_operator=True,glider_pilot=True)
    u2 = User(firstname='Ryszard',lastname='Manka',instructor=True,glider_pilot=True)
    u3 = User(firstname='Jacek',lastname='Sobolewski',instructor=True,winch_operator=True,airplane_pilot=True,glider_pilot=True)
    u4 = User(firstname='Maciej',lastname='Cymanski',glider_pilot=True)
    u5 = User(firstname='Mikołaj',lastname='Szyszka',glider_pilot=True)
    u6 = User(firstname='Maksymilian',lastname='Lewandowski',airplane_pilot=True,glider_pilot=True)
    u7 = User(firstname='Sebastian',lastname='Jabłonski',airplane_pilot=True,glider_pilot=True)
    u8 = User(firstname='Lech',lastname='Szaduro',winch_operator=True)

    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)
    db.session.add(p5)

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(u4)
    db.session.add(u5)
    db.session.add(u6)
    db.session.add(u7)
    db.session.add(u8)


    db.session.add(f1)
    db.session.add(f2)
    db.session.add(f3)
    # db.session.add(a1)
    # db.session.add(a2)
    # db.session.add(a3)

    db.session.commit()
    db.session.close()
    print("ok")

