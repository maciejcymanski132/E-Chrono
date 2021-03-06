from DB_Models import *


def populate_db():

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

    u0 = User(firstname='Passenger', lastname='')

    u1 = User(firstname='Roman', lastname='Berk', instructor=True,
              winch_operator=True, glider_pilot=True)
    u2 = User(firstname='Ryszard', lastname='Manka', instructor=True,
              glider_pilot=True)
    u3 = User(firstname='Jacek', lastname='Sobolewski', instructor=True,
              winch_operator=True, airplane_pilot=True, glider_pilot=True)
    u4 = User(firstname='Maciej', lastname='Cymanski', glider_pilot=True)
    u5 = User(firstname='Mikołaj', lastname='Szyszka', glider_pilot=True)
    u6 = User(firstname='Maksymilian', lastname='Lewandowski',
              airplane_pilot=True, glider_pilot=True)
    u7 = User(firstname='Sebastian', lastname='Jabłonski', airplane_pilot=True,
              glider_pilot=True)
    u8 = User(firstname='Lech', lastname='Szaduro', winch_operator=True)

    db.session.add(u0)

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(u4)
    db.session.add(u5)
    db.session.add(u6)
    db.session.add(u7)
    db.session.add(u8)

    db.session.commit()
    db.session.close()


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

    u0 = User(firstname='Passenger',lastname='',id=0)
    u1 = User(firstname='Roman',lastname='Berk',instructor=True,winch_operator=True,glider_pilot=True)
    u2 = User(firstname='Ryszard',lastname='Manka',instructor=True,glider_pilot=True)
    u3 = User(firstname='Jacek',lastname='Sobolewski',instructor=True,winch_operator=True,airplane_pilot=True,glider_pilot=True)
    u4 = User(firstname='Maciej',lastname='Cymanski',glider_pilot=True)
    u5 = User(firstname='Mikołaj',lastname='Szyszka',glider_pilot=True)
    u6 = User(firstname='Maksymilian',lastname='Lewandowski',airplane_pilot=True,glider_pilot=True)
    u7 = User(firstname='Sebastian',lastname='Jabłonski',airplane_pilot=True,glider_pilot=True)
    u8 = User(firstname='Lech',lastname='Szaduro',winch_operator=True)

    db.session.add(u0)
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(u4)
    db.session.add(u5)
    db.session.add(u6)
    db.session.add(u7)
    db.session.add(u8)

    db.session.commit()
    db.session.close()
