from datetime import datetime
from itertools import groupby

from .models import Booking, RoomCategory


# function to room availability
def check_room_availability(room, check_in, check_out):

    # initialise a list to storre available rooms
    avail_list = []

    # filter bookings by a specific room
    booking_list = Booking.objects.filter(room=room)

    # check if the room is booked on any of the selected dates within the 
    # the date range
    for booking in booking_list:
        if booking.check_in >check_out or booking.check_out <check_in:

            # if the selected dates do not intersect with any of the booked dates for that room
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


# funtion to process the data and return it in the format i wanted  
# not sure if it's the best but at least it works :) 
def process_data(data):
    
    # sort the data list based on 'room_type_id' key
    sorted_data = sorted(data, key=lambda x: x['room_type_id'])

    # group the sorted data by 'room_type_id' key
    grouped_data = groupby(sorted_data, key=lambda x: x['room_type_id'])

    # create a new list to store the grouped data
    result = []

    # iterate over the groups and append to the result list
    for room_type_id, group in grouped_data:
        
        room_data = list(group)
        
        # initialise an empty array to store available room ids
        room_ids = []

        # loop through the groped data to get return a list of each groups rooms
        for room in room_data:

            room_id = room['room_id']
            
            room_ids.append(room_id)

        # get room type object from RoomCategory model
        room_type = RoomCategory.objects.get(id=room_type_id)

        # append room_type and room_data to result array
        result.append({'room_type': room_type, 'rooms': room_ids,'room_data': room_data})

    # return an array of grouped data
    return result

    