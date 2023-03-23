from time import gmtime, strftime
from datetime import datetime, timedelta, timezone
from calendar import timegm
import ephem
import math
import bisect


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

def date_time_offset_to_utc_sec( datetime_str , offset_minutes ):
    print(f'datetime_str {datetime_str}')
    if offset_minutes.isdecimal():
        # flip the sign since method for calculating offset minutes is opposite
        # of the convention used for python datetime.timezone
        offset_minutes = -int(offset_minutes)
    else:
        offset_minutes = 0

    utc_offset = timezone(timedelta(minutes=offset_minutes))

    # construct a datetime object that is unaware of its timezone
    # this comes directly from the raw html form and is parsed
    # according to the following datetime code
    naive_datetime_object = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

    # now construct a new datetime object, this time passing it tzinfo
    aware_datetime_object = datetime(
        year = naive_datetime_object.year,
        month = naive_datetime_object.month,
        day = naive_datetime_object.day,
        hour = naive_datetime_object.hour,
        minute = naive_datetime_object.minute,
        second = naive_datetime_object.second,
        tzinfo = utc_offset
    )

    # generate a tuple of data, now converted to utc
    time_tuple = aware_datetime_object.utctimetuple()

    # convert this to seconds using the timegm function
    utc_seconds = timegm(time_tuple)

    return utc_seconds

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

    #define functions for previous and next dawn and dusk
    def previous_astronomical_dawn(sun_object):
        horizon_original = observer.horizon
        observer.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
        time_event = observer.previous_rising(sun, use_center=True) #Begin civil twilight
        observer.horizon = horizon_original
        return time_event

    def previous_astronomical_dusk(sun_object):
        horizon_original = observer.horizon
        observer.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
        time_event = observer.previous_setting(sun, use_center=True) #Begin civil twilight
        observer.horizon = horizon_original
        return time_event

    def next_astronomical_dawn(sun_object):
        horizon_original = observer.horizon
        observer.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
        time_event = observer.next_rising(sun, use_center=True) #Begin civil twilight
        observer.horizon = horizon_original
        return time_event

    def next_astronomical_dusk(sun_object):
        horizon_original = observer.horizon
        observer.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
        time_event = observer.next_setting(sun, use_center=True) #Begin civil twilight
        observer.horizon = horizon_original
        return time_event

    #place times of previous and next day events in sorted array
    sun_event_functions = [
    (previous_astronomical_dawn, "dawn"),
    (observer.previous_rising, "morning"),
    (observer.previous_transit, "evening"),
    (observer.previous_setting, "dusk"),
    (previous_astronomical_dusk, "night"),
    (next_astronomical_dawn, "dawn"),
    (observer.next_rising, "morning"),
    (observer.next_transit, "evening"),
    (observer.next_setting, "dusk"),
    (next_astronomical_dusk, "night")]

    times_day_events = []

    for sun_event_function, event_string in sun_event_functions:
        event_time = sun_event_function(sun)
        bisect.insort_left(times_day_events, [event_time, event_string])

    time_now = [observer.date, "now"]
    index_now = bisect.bisect_left(times_day_events, time_now)

    times_day_events.insert(index_now, time_now)

    #return progress + identity of event
    event_progress = \
    (times_day_events[index_now][0]-times_day_events[index_now-1][0]) / \
    (times_day_events[index_now+1][0]-times_day_events[index_now-1][0]) \

    if event_progress < (1/3):
        return "early " + times_day_events[index_now-1][1]
    elif event_progress > (2/3):
        return "late " + times_day_events[index_now-1][1]
    else:
        return "mid " + times_day_events[index_now-1][1]  

def spacetime_to_season(time_s, lat_deg, long_deg, elev_m):

    #initialize observer
    observer = ephem.Observer()
    observer.lat = str(lat_deg)
    observer.lon = str(long_deg)
    observer.elevation = elev_m
    observer.date = ephem.Date(datetime.utcfromtimestamp(time_s + 1738800)) #+20 days - 1/2 season

    if observer.lat >=0:
        season_event_functions = [
        (ephem.previous_vernal_equinox, "spring"),
        (ephem.previous_summer_solstice, "summer"),
        (ephem.previous_autumnal_equinox, "autumn"),
        (ephem.previous_winter_solstice, "winter"),
        (ephem.next_vernal_equinox, "spring"),
        (ephem.next_summer_solstice, "summer"),
        (ephem.next_autumnal_equinox, "autumn"),
        (ephem.next_winter_solstice, "winter")]
    else:
        season_event_functions = [
        (ephem.previous_vernal_equinox, "autumn"),
        (ephem.previous_summer_solstice, "winter"),
        (ephem.previous_autumnal_equinox, "spring"),
        (ephem.previous_winter_solstice, "summer"),
        (ephem.next_vernal_equinox, "autumn"),
        (ephem.next_summer_solstice, "winter"),
        (ephem.next_autumnal_equinox, "spring"),
        (ephem.next_winter_solstice, "summer")]

    times_season_events = []

    for season_event_function, event_string in season_event_functions:
        event_time = season_event_function(observer.date)
        bisect.insort_left(times_season_events, [event_time, event_string])

    time_now = [observer.date, "now"]
    index_now = bisect.bisect_left(times_season_events, time_now)

    times_season_events.insert(index_now, time_now)

    #return progress + identity of event
    event_progress = \
    (times_season_events[index_now][0]-times_season_events[index_now-1][0]) / \
    (times_season_events[index_now+1][0]-times_season_events[index_now-1][0]) \

    if event_progress < (1/3):
        return "early " + times_season_events[index_now-1][1]
    elif event_progress > (2/3):
        return "late " + times_season_events[index_now-1][1]
    else:
        return "mid " + times_season_events[index_now-1][1]  




