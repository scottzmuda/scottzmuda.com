from time import gmtime, strftime
import ephem


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

def spacetime_to_solar_elev_deg(time_s, lat_deg, long_deg):
    # convert unix time to a datetime object
    from datetime import datetime
    dt = datetime.utcfromtimestamp(time_s)
    
    # create a `location` object with the given coordinates
    location = ephem.Observer()
    location.lat = str(lat_deg)
    location.lon = str(long_deg)
    location.date = dt
    
    # calculate the solar elevation angle
    sun = ephem.Sun()
    sun.compute(location)
    elev_deg = float(sun.alt) * 180 / ephem.pi
    return elev_deg

