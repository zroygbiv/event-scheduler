"""
# Z.Roth

This file contains the primary components containing data
the user inputs into the scheduler.
Core hierarchy:
Date
 \
 Time
   \
  Event
    \
  Meal/Game_Night/Concert
"""

# Date
class Date:
    def __init__(self, m, d, y):
        self._day = d
        self._month = m
        self._year = y

    def get_day(self):
        return self._day

    def get_month(self):
        return self._month

    def get_year(self):
        return self._year

    def edit_date(self):
        print(":::New date:::")
        self._month = int(input("Month: "))
        self._day = int(input("Day: "))
        self._year = int(input("Year: "))

    def __lt__(self, other):
        """
        :type other: Date
        """
        if self._day < other._day:
            return True
        else:
            return False

    def __ge__(self, other):
        """
        :type other: Date
        """
        if self._day >= other._day:
            return True
        else:
            return False

# Time
class Time(Date):
    def __init__(self, s_h, s_m, s_me, e_h, e_m, e_me, *args, **kwargs):
        super(Time, self).__init__(*args, **kwargs)
        self._start_hour = s_h
        self._start_minute = s_m
        self._start_meridiem = s_me
        self._end_hour = e_h
        self._end_minute = e_m
        self._end_meridiem = e_me

    def edit_start_time(self):
        print(":::New start time:::")
        self._start_hour = int(input("Hour: "))
        self._start_minute = int(input("Minute: "))
        self._start_meridiem = input("AM/PM: ")

    def edit_end_time(self):
        print(":::New end time:::")
        self._end_hour = int(input("Hour: "))
        self._end_minute = int(input("Minute: "))
        self._end_meridiem = input("AM/PM: ")

# Event
class Event(Time):
    def __init__(self, title, loc, addr, att, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._title = title
        self._where = loc
        self._address = addr
        self._attendees = att

    def get_title(self):
        return self._title

    def get_month(self):
        month = super().get_month()
        return month

    def get_year(self):
        year = super().get_year()
        return year

    def add_attendee(self, new_attendee):
        if new_attendee not in self._attendees:
            self._attendees.remove(new_attendee)
        else:
            print("Person already exists!")

    def remove_attendee(self, attendee):
        if attendee in self._attendees:
            self._attendees.remove(attendee)
        else:
            print("Person was not found in list!")

    def update_title(self):
        self._title = input("Enter new event title: ")

    def update_location(self):
        self._where = input("Enter new location: ")

    def update_address(self):
        self._address = input("Enter new address: ")

    def __str__(self):
        if self is not None:
            return (f'\n:::Event Details:::\n'
                    f'Date: {self._month}/{self._day}/{self._year}\n'
                    f'Title: {self._title}\n'
                    f'Start time: {self._start_hour}:{self._start_minute} {self._start_meridiem}\n'
                    f'End time: {self._end_hour}:{self._end_minute} {self._end_meridiem}\n'
                    f'Location: {self._where}\n'
                    f'Address: {self._address}\n'
                    f'Persons: {", ".join(str(x) for x in self._attendees)}')

    def __eq__(self, other):
        """
        :type other: str
        """
        if self._title == other:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        :type other: str
        """
        if self._title != other:
            return False
        else:
            return True

# Meal
class Meal(Event):
    def __init__(self, *args, **kwargs):
        super(Meal, self).__init__(*args, **kwargs)
        self._food_items = []
        self._food_to_bring = []

    def add_food_item(self, item):
        if item not in self._food_items:
            self._food_items.append(item)
        else:
            print("Item already exists in list!")

    def add_food_to_bring(self, item):
        if item not in self._food_items:
            self._food_to_bring.append(item)
        else:
            print("Item already exists in list!")

    def remove_food_item(self, item):
        if item in self._food_items:
            self._food_items.remove(item)
        else:
            print("Item not found in list!")

    def __str__(self):
        event_info = super().__str__()
        return (f'{event_info}\n'
                f'Food: {", ".join(str(x) for x in self._food_items)}\n'
                f'What to bring: {", ".join(str(x) for x in self._food_to_bring)}\n')

# Concert
class Concert(Event):
    def __init__(self, *args, **kwargs):
        super(Concert, self).__init__(*args, **kwargs)
        self._performer = None
        self._ticket_cost = None

    def set_performer(self, perf):
        self._performer = perf

    def set_ticket_cost(self, ticket):
        self._ticket_cost = ticket

    def __str__(self):
        event_info = super().__str__()
        return (f'{event_info}\n'
                f'Performer: {self._performer}\n'
                f'Tickets: {self._ticket_cost}\n')

# Game_Night
class Game_Night(Event):
    def __init__(self, *args, **kwargs):
        super(Game_Night, self).__init__(*args, **kwargs)
        self._game_list = []

    def add_game(self, name):
        self._game_list.append(name)

    def __str__(self):
        event_info = super().__str__()
        return (f'{event_info}\n'
                f'Games to play: {", ".join(str(x) for x in self._game_list)}\n')
