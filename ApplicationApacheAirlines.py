
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 2 16:39:59 2025

@author: shahdalharthy
"""


import random
import string 


class Seat:
    """
    -Represents a single seat on the plane.
    -Attributes:
        seat_id (str) which is the unique ID of the seat, e.g., '1C'
        status (str) which is the current status ('F', 'R', 'X', 'S')
    """
    def __init__(self, seat_id, status):
        self.seat_id = seat_id
        self.status = status # 'F', 'X', 'S', or booking reference

    def is_avalible(self):
        # checks if seat is free and can be booked
        return self.status == 'F'

    def book(self, reference):
        # reserve the seat
        if self.status == 'F':
            self.status = reference  # store reference instead of 'R'
            return True
        return False

    def free(self):
        # frees the seat if it was booked
        if self.status not in ['F', 'X', 'S']:
            self.status = 'F'
            return True
        return False


class SeatMap:
    """
    -a class to manage all seats and their operations and the plane .
    -Attributes:
        columns (int): total number of seat rows (1 to 80)
        rows (list): row letters (A to F + X for aisle)
        seats (dict): maps seat IDs to Seat objects
    """
    def __init__(self, columns=80, rows=['A', 'B', 'C', 'X', 'D', 'E', 'F']):
        self.seats = {}
        self.columns = columns
        self.rows = rows
        self.aisles = ['X'] #aisle space — not bookable
        self.storage_seats = ['77D', '77E' ,'77F', '78D', '78E', '78F' ] 
        self.booking_references = set() 
        # Specific seats reserved for storage — not bookable
        self.initialize_seats()

    def initialize_seats(self):
        # initialize all seat objects with the appropriate status
        for col in range(1, self.columns+ 1):
            for row in self.rows:
                seat_id = f"{col}{row}"
                if seat_id in self.storage_seats:
                    status = 'S'  #storage
                elif row in self.aisles:
                    status = 'X'  # aisle  
                else:
                    status = 'F'
                self.seats[seat_id] = Seat(seat_id, status)

    def generate_unique_reference(self):
        while True:
            reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if reference not in self.booking_references:
                self.booking_references.add(reference)
                return reference


    def check_availability(self, seat_id):
        # Returns the current status of the seat
        seat = self.seats.get(seat_id)
        return seat.status if seat else "Invalid input"

    def book_seat(self, seat_id):
        # books a given seat (not storage or asile) 
        seat = self.seats.get(seat_id)
        if not seat:
            return "Invalid seat."
        if seat.status in ['X', 'S']:
            return f"Seat {seat_id} cannot be booked."
        if seat.status == 'F':
            reference = self.generate_unique_reference()
            seat.status = reference
            return f"Seat {seat_id} successfully booked with reference: {reference}"
        return f"Seat {seat_id} is already booked."

    def free_seat(self, seat_id):
        # free a booked seat if its not already free
        seat = self.seats.get(seat_id)
        if not seat:
            return "Invalid seat."
        if seat.status in ['X', 'S']:
            return f"Seat {seat_id} cannot be freed."
        if seat.free():
            return f"Seat {seat_id} is now free."
        return f"Seat {seat_id} is already free."

    def display_seat_map(self):
        # Prints the full seat map (status of each seat)
        print("  " + " ".join(self.rows))
        for col in range(1, self.columns + 1):
            col_display = [self.seats[f"{col}{row}"].status for row in self.rows]
            print(f"{col} " + " ".join(col_display))


    def view_booked_seats(self):
        booked = [seat_id for seat_id, seat in self.seats.items() if seat.status not in ['F', 'X', 'S']]
        if booked:
            print("Booked seats with references:")
            for seat_id in booked:
                print(f"{seat_id}: {self.seats[seat_id].status}")
        else:
            print("No seats are currently booked.")




class BookingSystem:
    """
    the main menu and user interactions.,
    """
    def __init__(self):
        self.seat_map = SeatMap()

    def run(self):
        while True:
            # Display the menu options
            print("\nApache Airlines Seat Booking System")
            print("1. Check availability of seat")
            print("2. Book a seat")
            print("3. Free a seat")
            print("4. Show booking status")
            print("5. Exit program")
            print("6. View all booked seats")  # Task 5
            
            choice = input("Select an option (1-5): ")

            if choice == "1":
                seat_id = input("Enter seat ID (e.g., 2A): ").upper()
                status = self.seat_map.check_availability(seat_id)
                print(f"Seat {seat_id} status: {status}")
            elif choice == "2":
                seat_id = input("Enter seat ID to book: ").upper()
                print(self.seat_map.book_seat(seat_id))
            elif choice == "3":
                seat_id = input("Enter seat ID to free: ").upper()
                print(self.seat_map.free_seat(seat_id))
            elif choice == "4":
                self.seat_map.display_seat_map()
            elif choice == "5":
                print("Exiting the program. Thank you!")
                break
            elif choice == "6":
                self.seat_map.view_booked_seats()
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    # Start the booking system
    system = BookingSystem()
    system.run()
