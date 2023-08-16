from datetime import datetime
from itertools import groupby

from django.db.models import Q

from .models import Booking, Property


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


# function that calculates the number of nights
def calc_number_of_nights(check_in, check_out):
    delta = check_in - check_out
    nights = abs(delta.days)
    return nights


# function to check if a user is eligible to write a review
def check_user_eligibility(user, property):

    # filter bookings by user and property
    bookings = Booking.objects.filter(Q(user=user)&Q(property=property))

    # initialise an empty eligibility list
    eligibility_list = []

    # loop through the user bookings
    for booking in bookings:

        # if user checked in append 'True' to the list else 'False'
        if booking.checked_in:
            eligibility_list.append(True)
        else:
            eligibility_list.append(False)
    
    # if any of the bookings returns true then the user is eligible to create a review
    return any(eligibility_list)
        

def perform_bnb_search(q):
    destructured = q.split(',')
    print(destructured)

    search_result = []
    for query in destructured:
        qs = Property.objects.filter(
            Q(title__icontains=query) | 
            Q(city__icontains=query) |
            Q(title__icontains=query) |
            Q(street_name__icontains=query) |
            Q(country__icontains=query) |
            Q(host__name__icontains=query)
        ).order_by('?').distinct()

        # search_result.append(qs)
        for item in qs:
            if item not in search_result:
                search_result.append(item)

        print(search_result)
    return search_result
    
