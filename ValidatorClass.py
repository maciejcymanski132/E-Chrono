from DB_Models import *
import datetime


class Validator:

    def __init__(self,flight):
        self.flight = flight

    def check_if_aircrafts_taken(self) -> bool:
        """
        Function checks if aircrafts chosen for beginning flight arent curently midair.
        :param flight:
        :return: Boolean value either aircrafts are free or not
        """
        active_flights = Chronometer.query.filter(Chronometer.active == True).all()
        for af in active_flights:
            if af.airplane.id == self.flight.airplane.id or af.glider.id == self.flight.glider.id:
                return True
        return False

    def check_if_pilots_midair(self) -> bool:
        """
        Function checks if pilot in flight beeing executed arent actually midair
        :param flight:
        :return:
        """
        mid_air_pilots=[]
        active_flights = Chronometer.query.filter(Chronometer.active == True).all()
        airplane_flights = AirplaneFlight.query.all()
        for f in active_flights:
            mid_air_pilots.append(f.pilot_passenger)
            mid_air_pilots.append(f.instructor)
        for f in airplane_flights:
            mid_air_pilots.append(f.airplane_pilot)

    def check_users_permissions(self) -> bool:
        """
        Checks if user is permitted to contribute in given way for example if
        instructor in flight record has instructor permission
        :param flight:
        :return: Boolean value either users fit or not
        """
        if self.flight.instructor:
            if not self.flight.instructor.instructor:
                return False
        if self.flight.pilot_passenger.id != 0:
            if not self.flight.pilot_passenger.glider_pilot:
                return False
        if self.flight.pilot_passenger.id == 0:
            if not self.flight.instructor:
                return False
        if self.flight.winch_operator:
            if not self.flight.winch_operator.winch_operator:
                return False
        if self.flight.tow_pilot:
            if not self.flight.tow_pilot.airplane_pilot:
                return False
        return True

    def check_start_type(self) -> bool:
        """
        Function checks if start type matches with other fields
        for example if start type is winch launch field flight.airplane should be
        none
        W - winch start
        S - tow pull start (S for samolot in pol.)
        :param flight:
        :return:
        """
        if self.flight.start_type == 'W' and self.flight.tow_pilot:
            return False
        if self.flight.start_type == 'S' and self.flight.winch_operator:
            return False
        if self.flight.start_type == 'S' and not self.flight.airplane:
            return False
        return True

    def validate_operators(self) -> bool:
        """
        Checks if there is one and only one staff member executing launch
        :param flight:
        :return: Boolean value
        """
        if (self.flight.tow_pilot and self.flight.winch_operator) or (not self.flight.tow_pilot and not self.flight.winch_operator):
            return False
        return True

    def check_duplicate_ids(self) -> bool:
        """
        Checks if there are any duplicate users taking part in flight
        :param flight:
        :return:
        """
        crew = [self.flight.instructor,self.flight.pilot_passenger,self.flight.winch_operator,self.flight.tow_pilot]
        for member in crew:
            if member != None and crew.count(member) > 1:
                return False
        return True

    def validate_flight(self):
        """
        Checks if flight isnt already active
        :param flight:
        :return:
        """
        active_flights = [f[0] for f in Chronometer.query. \
            filter(Chronometer.active == True).with_entities(
            Chronometer.flight_nr).all()]
        if self.flight.flight_nr not in active_flights \
                and self.flight.time_of_start == "-" \
                and not self.check_if_aircrafts_taken():
            return True

    def validate_chrono_table(self) -> bool:
        """
        Wraps together previous functions to one para-script
        :param flight:
        :return:
        """
        if not self.check_duplicate_ids():
            return False
        if self.check_if_aircrafts_taken():
            return False
        if not self.check_users_permissions():
            return False
        if not self.check_start_type():
            return False
        if not self.validate_operators():
            return False
        return True


def flip_booleans(arguments):
    """
    In html you cannot simply state boolean value as tag value so this is function
    which swaps string 'True' to boolean value
    :param arguments:
    :return:
    """
    for key,value in arguments.items():
        if value == 'true':
            arguments[key] = True
        if value == 'false':
            arguments[key] = False


def time_difference(time1, time2):
    t1 = datetime.datetime.strptime(time1, "%H:%M")
    t2 = datetime.datetime.strptime(time2, "%H:%M")
    return str(t2 - t1)[0:4]


def chrono_to_airplane(chrono_object):
    """
    Function which converses one table record to another one for estetic purposes.
    :param chrono_object:
    :return:
    """
    return AirplaneFlight(
        flight_nr=chrono_object.flight_nr,
        time_of_start=chrono_object.time_of_start,
        airplane_pilot=chrono_object.tow_pilot.id,
        airplane=Airplane.query.filter(Airplane.id == chrono_object.airplane.id).first().name,
    )