from datetime import datetime as dt
from datetime import timedelta as td
from calendar import monthrange as ndays
import re
import os

import tables
from pylab import *
from hisparc.publicdb import download_data

from remove_dups_hisparcdata import remove_dups
from remove_dups_weatherdata import remove_dups_weatherdata
from check_if_weather import check_if_weather


def down_data_in_parts(station_id, user_start_date_data_interval,
                       user_stop_date_data_interval):
    """ Download HiSPARC data in parts

    This function will split the downloading of data into months, making
    one file for each part. This may make working with large data sets easier
    on slower computers.

    The end date is not included, it is not 'up to and including ..'
    So start=dt(2011, 6, 29), stop=dt(2011, 6, 30)
    Only downloads data from 29th June.

    """
    # split user input date strings
    start_list = re.split(',', user_start_date_data_interval)
    stop_list = re.split(',', user_stop_date_data_interval)

    # turn the list of strings into integers
    start_list_int = [int(x) for x in start_list]
    stop_list_int = [int(x) for x in stop_list]

    # turn the date list into date objects
    start_date = dt(start_list_int[0], start_list_int[1], start_list_int[2])
    stop_date = dt(stop_list_int[0], stop_list_int[1], stop_list_int[2])

    downloaded_data_files = []

    if start_date >= end_date:
        print 'Error: Start date is after stop date!'
    elif end_date >= dt.today():
        print 'Error: End date is after today!'
    elif start_date < dt(2004, 1, 1):
        print 'Error: Start date is before the start of the HiSPARC project!'
    else:
        for start, stop in monthrange(start_date, stop_date):
            filename = download_part(station_id, start, stop)
            downloaded_data_files.append(filename)
    print 2 * "\a"
    return downloaded_data_files


def monthrange(start, stop):
    """ A generator function that yields datetime objects in ranges of months

    If start and stop are more than 31 days apart the interval is split into
    months. The first will be from start until the end of its month, then
    each month upto the month of stop, and finally from the start of that
    month until stop.

    """
    a_day = td(days = 1)
    if (stop - start).days < 31:
        yield start, stop
        return
    else:
        cur = start + td(days = ndays(start.year, start.month)[1] - start.day + 1)
        yield start, cur
        while cur + td(days = ndays(cur.year, cur.month)[1]) < stop:
            yield cur, cur + td(days = ndays(cur.year, cur.month)[1])
            cur += td(days = ndays(cur.year, cur.month)[1])
        yield cur, stop
        return
            

def download_part(station_id, start, stop):
    """ Download HiSPARC data from start till stop

    """
    hisp_station = int(station_id)
    tree = '/s' + station_id
    path = 'data.root.s' + station_id
    filename = 'data_s%d_%s_%s.h5' % (hisp_station,
                                      start.strftime('%Y,%m,%d'),
                                      stop.strftime('%Y,%m,%d'))
    with tables.openFile(filename, 'w') as data:
        download_data(data, tree, hisp_station, start, stop)
        remove_dups(data, eval(path))
        weather_data_in_file = check_if_weather(data, filename)
        if weather_data_in_file:
            remove_dups_weatherdata(data, eval(path))
    print ''
    print "'" + filename + "' has downloaded."
    print 'You can find it at the location: ' + os.getcwd()
    print ''
    return filename
