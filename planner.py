"""
# Z. Roth
This file contains the "logic" or "manager" class called Planner.
Responsibilities:
-Handling user input
-Calling important class methods
-Displaying information to the user
-Conducting overall flow of the program.
One structure containing two event_schedulers (arrays of LLL)
One structure for storage of user comments (BST of LLL)
"""

from event import *
from ds import *
import numpy
import time
import calendar

class Planner:
    def __init__(self):
        self._events_attended_2022 = numpy.empty(12, dtype=Linked_List)
        for month in range(12):
            self._events_attended_2022[month] = Linked_List()

        self._events_attended_2023 = numpy.empty(12, dtype=Linked_List)
        for month in range(12):
            self._events_attended_2023[month] = Linked_List()

        self._completed_events_db = Tree()

    # new search router/logic
    def new_search(self, choice):
        # add new event
        if choice == 1:
            self.new_event_menu()
            choice = int(input("Enter choice: "))
            event = self.create_new_event(choice)
            self.add_event(event)
            print("\n+++Event added to calendar+++")
            time.sleep(1)
        # remove event
        elif choice == 2:
            title = input("Enter title of event: ")
            self.remove_event(title)
        # print next upcoming event
        elif choice == 3:
            self.display_upcoming_event()
        # participate in next event
        elif choice == 4:
            # get upcoming event
            next_event = self.get_upcoming_event()
            # if event is not None
            if next_event is not None:
                # add event to tree node; tree node added to tree
                self._completed_events_db.add_tree_node(next_event)
                # find tree node with completed event data
                completed_event = self._completed_events_db.find_tree_node(next_event)
                # remove completed event from scheduler
                self.remove_completed_event(next_event)

                if completed_event is not None:
                    # add comments to completed event tree node
                    self.add_comments_to_completed_event(completed_event)
            else:
                print("\n\t--NO EVENTS SCHEDULED--")
                time.sleep(1)

        # refer to notes of a completed event
        elif choice == 5:
            past_title = input("Enter title of past event: ")
            print("\n\tSEARCHING...\n")
            time.sleep(1)
            result = self.find_past_event(past_title)
            if result is not None:
                past_event = self._completed_events_db.find_tree_node(past_title)

                if past_event is not None:
                    self._completed_events_db.display_tree_node_comments(past_event)
                    time.sleep(4)
            else:
                print("\t--NO MATCH FOUND--")
                time.sleep(1)

        # print calendar by month or by year
        elif choice == 6:
            filter_choice, year_choice, month = self.display_decider()

            if filter_choice == 1:
                if year_choice == 1:
                    self.display_planner(month, 2022)
                elif year_choice == 2:
                    self.display_planner(month, 2023)

            elif filter_choice == 2:
                if year_choice == 1:
                    self.display_planner(0, 2022)
                if year_choice == 2:
                    self.display_planner(0, 2023)

    # main menu display
    def main_menu(self):
        print("\n:::HOLIDAY EVENT SCHEDULER:::")
        print("1. Add new event")
        print("2. Remove an event")
        print("3. Print next upcoming event")
        print("4. Participate in next event")
        print("5. Search comments of completed event")
        print("6. Print calendar")
        print("7. Exit scheduler\n")

    # new event submenu display
    def new_event_menu(self):
        print("\n\t:::ADD AN EVENT TO SCHEDULER:::\n")
        print("1. Meal")
        print("2. Game Night")
        print("3. Concert\n")

    def user_choice(self):
        while True:
            try:
                choice = input("Enter here: ")
                cap_choice = choice.capitalize()
                if cap_choice == "Yes" or cap_choice == "No":
                    break
                else:
                    raise ValueError

            except ValueError:
                print("\n\t:::INVALID INPUT!::: ")
                print("\tPlease enter 'Yes' or 'No'")
                time.sleep(1)

        return cap_choice

    # input date data
    def new_date(self):
        while True:
            date = input("Enter date (MM/DD/YYYY): ")
            try:
                month, day, year = map(int, date.split('/'))
                break
            except:
                print("Date entered incorrectly, format is MM/DD/YYYY")

        return month, day, year

    # input time data
    def new_time(self):
        while True:
            time_input = input("Enter time (00:00): ")
            try:
                hour, minute = map(int, time_input.split(':'))
                break
            except:
                print("Time entered incorrectly, format is 00:00")

        while True:
            try:
                meridiem = input("AM/PM: ")
                if meridiem == "AM" or meridiem == "PM":
                    break
                else:
                    raise ValueError
            except ValueError:
                print("\n\t:::INVALID INPUT!::: ")
                print("\tPlease enter 'AM' or 'PM'\n")

        return hour, minute, meridiem

    # create new date and time
    def new_date_time(self):
        month, day, year = self.new_date()
        print("\n:::Start Time:::")
        start_hr, start_min, start_meridiem = self.new_time()
        print("\n:::End Time:::")
        end_hr, end_min, end_meridiem = self.new_time()

        return month, day, year, start_hr, start_min, start_meridiem, \
            end_hr, end_min, end_meridiem

    # create new event
    def create_new_event(self, choice):
        mo, dy, yr, s_hr, s_min, s_mer, e_hr, e_min, e_mer = self.new_date_time()

        title = input("Title of event: ")
        loc = input("Event location: ")
        address = input("Event address: ")

        print("#Enter each person attending event, or enter 'Done' when finished: ")
        count = 1
        attendees = []

        while True:
            new_person = input("Person " + str(count) + ": ")
            cap_new_person = new_person.capitalize()
            if cap_new_person != "Done":
                attendees.append(new_person)
                count = count + 1
            else:
                break

        # route based on event type, input remaining fields of relevance
        if choice == 1:
            new_event = Meal(title, loc, address, attendees, s_hr, s_min, s_mer,
                             e_hr, e_min, e_mer, mo, dy, yr)

            print("Will this be at a restaurant? (Yes/No): ")
            dine_out = self.user_choice()

            if dine_out == "No":
                print("\n#Enter all food items to bring (if applicable), "
                      "enter 'Done' when finished")
                while True:
                    new_food_item = input("Food item: ")
                    new_food_item.capitalize()

                    if new_food_item != "Done":
                        new_event.add_food_item(new_food_item)

                        print("Are you bringing this food? (yes/no): ")
                        response = self.user_choice()
                        if response == "Yes":
                            new_event.add_food_to_bring(new_food_item)
                    else:
                        break

        if choice == 2:
            new_event = Game_Night(title, loc, address, attendees, s_hr, s_min, s_mer,
                                   e_hr, e_min, e_mer, mo, dy, yr)

            while True:
                name = input("Enter a game name: ")
                new_event.add_game(name)
                print("Add another game? (yes/no): ")
                add_another = self.user_choice()
                if add_another != "Yes":
                    break

        if choice == 3:
            new_event = Concert(title, loc, address, attendees, s_hr, s_min, s_mer,
                                e_hr, e_min, e_mer, mo, dy, yr)

            performer = input("Performer: ")
            new_event.set_performer(performer)
            ticket_cost = int(input("Ticket cost: "))
            new_event.set_ticket_cost(ticket_cost)

        return new_event

    # add event to planner
    def add_event(self, event):
        month = event.get_month() - 1

        if event.get_year() == 2022:
            self._events_attended_2022[month].append(event)
            self._events_attended_2022[month].sort()

        elif event.get_year() == 2023:
            self._events_attended_2023[month].append(event)
            self._events_attended_2023[month].sort()

    # remove an event
    def remove_event(self, title):
        for month in range(12):
            if self._events_attended_2022[month] is not None:
                if self._events_attended_2022[month].remove(title) is True:
                    print("\n\t--Event removed!--")
                    time.sleep(1)
                    return

        for month in range(12):
            if self._events_attended_2023[month] is not None:
                if self._events_attended_2023[month].remove(title) is True:
                    print("\n\t--Event removed!--")
                    time.sleep(1)
                    return

        print("\n\t--NO MATCH FOUND--")
        time.sleep(1)

    def find_past_event(self, title):
        past_event = self._completed_events_db.find_tree_node(title)

        return past_event

    # get next event in scheduler
    def get_upcoming_event(self):
        event_found_2022 = False
        for month in range(12):
            if self._events_attended_2022[month].get_head() is not None:
                event_found_2022 = True
                index = month
        if event_found_2022 is True:
            next_event = self._events_attended_2022[index].get_head()
            print(next_event)
            return next_event

        event_found_2023 = False
        for month in range(12):
            if self._events_attended_2023[month].get_head() is not None:
                event_found_2023 = True
                index = month
        if event_found_2023 is True:
            next_event = self._events_attended_2023[index].get_head()
            print(next_event)
            return next_event

        return None

    def add_comments_to_completed_event(self, completed_event):
        print("Now that you've participated in this event...")
        print("It's time to leave comments/thoughts/suggestions:\n")
        comment_num = 1
        while True:
            print(f'Comment {comment_num}: ')
            comment = input()
            completed_event.add_comment(comment)
            print("Would you like to add another comment? (yes/no): ")
            choice = self.user_choice()
            if choice == "No":
                break
            elif choice == "Yes":
                comment_num = comment_num + 1

    # remove a completed event from scheduler
    def remove_completed_event(self, completed_event):
        for month in range(12):
            if self._events_attended_2022[month].get_head() == completed_event:
                self._events_attended_2022[month].remove(completed_event)
                print("*******Participating*******")
                time.sleep(2)
                print("\n\t--Event completed!--\n")
                time.sleep(2)
                return

        for month in range(12):
            if self._events_attended_2023[month].get_head() == completed_event:
                self._events_attended_2023[month].remove(completed_event)
                print("*******Participating*******")
                time.sleep(2)
                print("\n\t--Event completed!--\n")
                time.sleep(2)
                return

    # display next upcoming event
    def display_upcoming_event(self):
        event_found_2022 = False
        for month in range(12):
            if self._events_attended_2022[month].get_head() is not None:
                event_found_2022 = True
                index = month

        if event_found_2022 is True:
            print("\n\t:::Next Upcoming Event:::")
            print(self._events_attended_2022[index].get_head())
            time.sleep(2)
            return

        event_found_2023 = False
        for month in range(12):
            if self._events_attended_2023[month].get_head() is not None:
                event_found_2023 = True
                index = month
        if event_found_2023 is True:
            print("\t:::Next Upcoming Event:::\n")
            print(self._events_attended_2023[index].get_head())
            time.sleep(2)
            return

        print("\n\t--NO EVENTS SCHEDULED--")
        time.sleep(1)

    # display logic function
    def display_decider(self):
        while True:
            try:
                print("\n:::Print Calendar:::")
                print("1. By month")
                print("2. By year")
                filter_choice = int(input("\nEnter choice: "))
                if filter_choice < 1 or filter_choice > 2:
                    raise ValueError

                print("\n:::Choose calendar year:::")
                print("1. 2022")
                print("2. 2023")
                year_choice = int(input("\nEnter choice: "))
                if year_choice < 1 or year_choice > 2:
                    raise ValueError

                if filter_choice == 1:
                    month = int(input("Enter a month (1-12): "))
                    if month < 1 or month > 12:
                        raise ValueError
                else:
                    month = 0
                break

            except ValueError:
                print("\n\t:::INVALID INPUT!::: ")
                print("\tPlease choose correctly from the menu options")
                time.sleep(1)

        return filter_choice, year_choice, month

    # display all events in a month, either 2022 or 2023
    def display_planner(self, month, year):
        if month == 0:
            if year == 2022:
                print("\n\t:::Event Calendar 2022:::\n")
                for month in range(1, 13):
                    index = month - 1
                    print("\t       ", calendar.month_name[month])
                    if self._events_attended_2022[index].get_head() is not None:
                        month
                        print(self._events_attended_2022[index])
                        time.sleep(2)
                    else:
                        print("\t--NO EVENTS SCHEDULED--\n")
                        time.sleep(1)

            elif year == 2023:
                print("\n\t:::Event Calendar 2023:::\n")
                for month in range(1, 13):
                    index = month - 1
                    print("\t       ", calendar.month_name[month])
                    if self._events_attended_2023[index].get_head() is not None:
                        month
                        print(self._events_attended_2023[index])
                        time.sleep(2)
                    else:
                        print("\t--NO EVENTS SCHEDULED--\n")
                        time.sleep(1)
        else:
            index = month - 1
            if year == 2022:
                print("\n:::Upcoming Events:::")
                if self._events_attended_2022[index].get_head() is not None:
                    print(self._events_attended_2022[index])
                    time.sleep(1)
                else:
                    print("\n\t--NO EVENTS SCHEDULED--")
                    time.sleep(1)

            elif year == 2023:
                print("\n\t:::Upcoming Events:::")
                if self._events_attended_2023[index].get_head() is not None:
                    print(self._events_attended_2023[index])
                    time.sleep(1)
                else:
                    print("\n\t--NO EVENTS SCHEDULED--")
                    time.sleep(1)
