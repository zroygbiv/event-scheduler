"""
# Z.Roth

This file is ground zero where a Planner object is created, the user
chooses from menu of options which the Planner then takes and executes
necessary operations. The user can complete repeated operations or exit
the program when finished.
"""

from planner import *
import time

def main():
    event_planner = Planner()

    while True:
        event_planner.main_menu()

        try:
            choice = int(input("Enter choice: "))
            if 0 < choice < 8:
                # exit program
                if choice == 7:
                    print("Exiting program...\n")
                    time.sleep(1)
                    break
                else:
                    event_planner.new_search(choice)
            else:
                raise ValueError

        except ValueError:
            print("\n\t:::INVALID INPUT!::: ")
            print("\tPlease choose from the menu options (1-8) ")
            time.sleep(1)

if __name__ == '__main__':
    main()
