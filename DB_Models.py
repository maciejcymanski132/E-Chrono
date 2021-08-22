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
                        pilot_instructor = 1,
                        passenger_student = 1,
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
                        pilot_instructor = '2',
                        passenger_student = '2',
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
                        pilot_instructor = '3',
                        passenger_student = '3',
                        glider = 'Puchacz-3351',
                        airplane = 'SP-CAS'
        )

    db.session.add(f1)
    db.session.add(f2)
    db.session.add(f3)
    db.session.commit()
    db.session.close()
    print("ok")

