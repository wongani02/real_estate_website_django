from datetime import datetime
from itertools import groupby

from .models import Booking


# function to room availability
def check_room_availability(bnb, check_in, check_out):

    # initialise a list to storre available rooms
    avail_list = []

    # filter bookings by a specific room
    booking_list = Booking.objects.filter(property=bnb)

    # check if the room is booked on any of the selected dates within the 
    # the date range
    for booking in booking_list:

        if booking.check_in >check_out or booking.check_out <check_in:

            # if the selected dates do not intersect with any of the booked dates for that bnb
            # flag it as available 
            avail_list.append(True)
            
        else:
            # else flag it as false
            avail_list.append(False)

    # return boolean 
    # this will only return true if selected dates are completely free
    # this function is pretty much the engine of the whole booking functionality :)
    return all(avail_list)


# function to format the date
def format_dates(date_value):
    
    # split the date by ' to '
    split_date = date_value.split(' to ')
    
    # initialise a list to store the formatted dates
    dates = []

    # loop through the split dates
    for date in split_date:

        # format date with the striptime method
        formated_date = datetime.strptime(date, "%Y-%m-%d").date()
        
        # append the formatted date to the date array
        dates.append(formated_date)

    # return formatted dates
    return dates[0], dates[1]


def calc_number_of_nights(check_in, check_out):
    delta = check_in - check_out
    nights = abs(delta.days)
    return nights

