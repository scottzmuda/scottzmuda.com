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
    
    #initialize variables
    gregorian_time = datetime.utcfromtimestamp(time_s)
    gregorian_time_before = datetime.utcfromtimestamp(time_s - 43200)
    altHorizonCross = math.radians(-5/6)
    altLightDarkTransition = math.radians(-18)
    sun = ephem.Sun()


    # create an observer at time of interest
    observer = ephem.Observer()
    observer.lat = str(lat_deg)
    observer.lon = str(long_deg)
    observer.elevation = elev_m
    observer.date = ephem.Date(gregorian_time)
    sun.compute(observer)
    altCurrent = sun.alt

    # change observer to half a day before
    observer.date = ephem.Date(gregorian_time_before)
    sun.compute(observer)

    # find time and altitudes of solar midday and midnight.
    # determine hasDay and hasNight
    nearestSolarMidday = observer.next_transit(ephem.Sun())
    nearestSolarMidnight = observer.next_antitransit(ephem.Sun())

    observer.date = nearestSolarMidday
    sun.compute(observer)
    altSolarMidday = sun.alt
    hasDay = True if altSolarMidday > altHorizonCross else False

    observer.date = nearestSolarMidnight
    sun.compute(observer)
    altSolarMidnight = sun.alt
    hasNight = True if altSolarMidnight < altLightDarkTransition else False

    # find distances to solar events
    distanceMidnight = abs(altCurrent - altSolarMidnight)
    distanceDarkLightTransition = abs(altCurrent - altLightDarkTransition)
    distanceHorizonCrosss = abs(altCurrent - altHorizonCross)
    distanceMidday = abs(altCurrent - altSolarMidday)

    # find nearest solar event
    if not hasDay and not hasNight:
        return "twilight"

    elif hasDay and  distanceMidday < distanceHorizonCrosss:
        return "midday"

    elif hasNight and  distanceMidnight < distanceDarkLightTransition:
        return "midnight"

    elif hasDay and not hasNight:
        return "sunrise or sunset"

    elif hasNight and not hasDay:
        return "dawn or dusk"

    elif distanceHorizonCrosss < distanceDarkLightTransition:
        return "sunrise or sunset"

    else:
        return "dawn or dusk"

