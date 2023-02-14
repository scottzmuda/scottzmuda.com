from time import gmtime, strftime
from datetime import datetime
import ephem
import math


def utc_sec_to_date_time( utc_sec ):
    if not utc_sec:
        return ""
    
    # convert utc seconds to time structure
    utc_time_fields = gmtime(utc_sec)

    # parse individual fields to desired formatting
    year = utc_time_fields.tm_year
    month_name = strftime("%B", utc_time_fields).lower()
    day_of_month = format_day_of_month(utc_time_fields.tm_mday)
    hours = format_hours_remove_leading_zero( strftime("%I", utc_time_fields ))
    minutes = strftime("%M", utc_time_fields)
    am_pm = strftime("%p", utc_time_fields).lower()

    # then recombine into formatted string
    res_time_string = f'{year}, {month_name} {day_of_month}, \
        {hours}:{minutes} {am_pm} [utc]'

    return res_time_string

# helper function to ensure days of months get correct suffix added to them
def format_day_of_month( day_int ):
    if day_int <= 0 or day_int > 31:
        return ""
    
    match day_int:
        case 1:
            return "1st"
        case 2:
            return "2nd"
        case 3:
            return "3rd"
        case 21:
            return "21st"
        case 22:
            return "22nd"
        case 23:
            return "23rd"
        case 31:
            return "31st"
        case _:
            return f"{day_int}th"
        
# Python's time library does not contain a built in way to trim leading 0s
def format_hours_remove_leading_zero( hours_str ):
    if not hours_str or not hours_str.isdecimal():
        return ""
    
    hours_int = int(hours_str)

    return f"{hours_int}"

def spacetime_to_sun_based_time(time_s, lat_deg, long_deg, elev_m):
    
    #initialize observer
    observer = ephem.Observer()
    observer.lat = str(lat_deg)
    observer.lon = str(long_deg)
    observer.elevation = elev_m
    observer.date = ephem.Date(datetime.utcfromtimestamp(time_s))

    #initialize sun
    sun = ephem.Sun()
    sun.compute(observer)

    #get times of nearest solar events (still need to account for exceptions)
    times_sun_events = []
    times_sun_events.append(observer.date - observer.previous_transit(ephem.Sun()))
    times_sun_events.append(observer.date - observer.previous_antitransit(ephem.Sun()))
    times_sun_events.append(observer.date - observer.previous_setting(ephem.Sun()))
    times_sun_events.append(observer.date - observer.previous_rising(ephem.Sun()))
    times_sun_events.append(observer.date - observer.next_transit(ephem.Sun()))
    times_sun_events.append(observer.date - observer.next_antitransit(ephem.Sun()))
    times_sun_events.append(observer.date - observer.next_setting(ephem.Sun()))
    times_sun_events.append(observer.date - observer.next_rising(ephem.Sun()))

    #find nearest event
    nearest_event_index = min(enumerate(times_sun_events), key=lambda x: abs(x[1]))[0]

    #find magnitude of time delta
    if abs(times_sun_events[nearest_event_index])*24 < 1:
        magnitude_string = "a litte bit "
    elif abs(times_sun_events[nearest_event_index])*24 < 3:
        magnitude_string = "a good bit "
    else:
        magnitude_string = "a good while "     

    #find sign of time delta
    if times_sun_events[nearest_event_index] > 0:
        relation_string = "after "
    else:
        relation_string = "before "

    #determine identity of sun event
    if nearest_event_index in [0, 4]:
            return magnitude_string + relation_string + "midday"
    if nearest_event_index in [1, 5]:
            return magnitude_string + relation_string + "midnight"
    if nearest_event_index in [2, 6]:
            return magnitude_string + relation_string + "sunset"
    if nearest_event_index in [3, 7]:
            return magnitude_string + relation_string + "sunrise"