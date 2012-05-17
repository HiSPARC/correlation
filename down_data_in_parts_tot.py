from datetime import datetime as dt
import re
import os

import tables
from pylab import *
from hisparc.publicdb import download_data

from remove_dups_hisparcdata import remove_dups
from remove_dups_weatherdata import remove_dups_weatherdata
from question_is_digit import question_is_digit
from start_end_day_of_the_month import start_end_day_of_the_month
from check_if_weather import check_if_weather


def diff_month(d1, d2):
    """Calculate the number of months within a time interval"""
    return (d2.year - d1.year)*12 + d2.month - d1.month + 1


def down_data_in_parts(user_hisparc_station_id, user_start_date_data_interval,
                       user_stop_date_data_interval):
    """ Download HiSPARC data in parts

    The end date is not included, it is not 'up to and including ..'
    So start=dt(2011, 6, 29), stop=dt(2011, 6, 30)
    Only downloads data from 29th June.

    """

    # find out how many days of data the user wants to download

    # split user input date strings
    start_list = re.split(',', user_start_date_data_interval)
    stop_list = re.split(',', user_stop_date_data_interval)

    # turn the list of strings into integers
    start_list_int = [int(x) for x in start_list]
    stop_list_int = [int(x) for x in stop_list]

    # turn the date list into date objects
    start_date = dt(start_list_int[0], start_list_int[1], start_list_int[2])
    end_date = dt(stop_list_int[0], stop_list_int[1], stop_list_int[2])

    # make list of filenames with downloaded data
    downloaded_data_files = []

    if start_date <= end_date and end_date <= dt.today() and start_date > dt(1998, 1, 1):

        delta = end_date - start_date
        days = delta.days

        # If the pytable contains more than a month of data it gets too large to handle for my pc
        if days <= 31:
            start = dt(start_list_int[0], start_list_int[1], start_list_int[2])
            stop = dt(stop_list_int[0], stop_list_int[1], stop_list_int[2])
            filename = download_part(user_hisparc_station_id, start, stop)
            downloaded_data_files.append(filename)

        # i.e. the time interval spans MORE than 31 days
        else:
            check = stop_list_int[1] + stop_list_int[2]

            # i.e. the timeinterval spans over two years and the stop date is not the first day of the last year (in that case the user intends to download one whole year)
            if start_list_int[0] != stop_list_int[0] and check != 2:

                # make a list of years to loop through
                nyears = range(0, stop_list_int[0] - start_list_int[0] + 1) # e.g. [0,1]
                years = [start_list_int[0] + x for x in nyears] # e.g. [2010,2011]

                for y in years:
                    # For the first year download first month
                    if y == years[0]:
                        if start_list_int[1] != 12:
                            start = dt(y, start_list_int[1], start_list_int[2])
                            stop = dt(y, start_list_int[1] + 1, 1)
                            filename = download_part(user_hisparc_station_id, start, stop)
                            downloaded_data_files.append(filename)
                        elif start_list_int[1] == 12:
                            start = dt(y, start_list_int[1], start_list_int[2]),
                            stop = dt(y + 1, 1, 1)
                            filename = download_part(user_hisparc_station_id, start, stop)
                            downloaded_data_files.append(filename)
                        # download the rest of the months of the first year
                        # condition is necessary because if the december is the only month of the first year we are alredy done
                        if start_list_int[1] != 12:
                            months = range(start_list_int[1] + 1, 13)
                            for m in months:
                                first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], m)
                                if m != 12:
                                    start = dt(start_list_int[0], m, first_last_day_of_the_month[0])
                                    stop = dt(y, m + 1, 1)
#                                    stop = dt(start_list_int[0], j+1, 1)
                                if m == 12:
                                    start = dt(y, m, first_last_day_of_the_month[0])
                                    stop = dt(y + 1, 1, 1)
#                                    start = dt(start_list_int[0], j, first_last_day_of_the_month[0])
#                                    stop = dt(start_list_int[0]+1, 1, 1)
                                filename = download_part(user_hisparc_station_id, start, stop)
                                downloaded_data_files.append(filename)

                    # If we are not in the first and last year
                    if y != years[-1] and y != years[0]:
                        months = range(1, 13)  # [1, 2, ... 12]
                        for m in months: # Download data for all months
                            first_last_day_of_the_month = start_end_day_of_the_month(y, m)
                            if m != 12:
                                start = dt(y, m, first_last_day_of_the_month[0])
                                stop = dt(y, m + 1, 1)
                            if m == 12:
                                start = dt(y, m, first_last_day_of_the_month[0])
                                stop = dt(y + 1, 1, 1)
                            filename = download_part(user_hisparc_station_id, start, stop)
                            downloaded_data_files.append(filename)

                    # If we are in the last year
                    if y == years[-1]:
                        # make list of months
                        nmonths = diff_month(date(y,1,1), end_date)
                        months = range(1, nmonths+1)

                        for m in months:
                            first_last_day_of_the_month = start_end_day_of_the_month(y, m)
                            start = dt(y, m, first_last_day_of_the_month[0])
                            if m != months[-1]: # if we are not in the last month of the last year
                                stop = dt(y, m + 1, 1)
                            # if we are in the last month of the last year
                            if m == months[-1]:
                                stop = dt(y, stop_list_int[1], stop_list_int[2])
                                # stop = dt(i, j, stop_list_int[2])
                            filename = download_part(user_hisparc_station_id, start, stop)
                            downloaded_data_files.append(filename)

            # i.e. the time interval is shorter than one year or equal to one year
            else:
                nmonths = diff_month(start_date, end_date)
                if stop_list_int[2] == 1:
                    months = range(start_list_int[1], start_list_int[1] + nmonths - 1)
                else:
                    months = range(start_list_int[1], start_list_int[1] + nmonths)

                for m in months:
                    first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], m)
                    # finish first month of data
                    if m == months[0]:
                        start = dt(start_list_int[0], m, start_list_int[2])
                        stop = dt(stop_list_int[0], m + 1, 1)
                    # if we are NOT downloading the first month of data and also NOT the last month of data
                    if m != months[0] and m != months[-1]:
                        start = dt(start_list_int[0], m, first_last_day_of_the_month[0])
                        stop = dt(stop_list_int[0], m + 1, 1)
                    # if we are downloading the last month of data
                    if m == months[-1]:
                        if stop_list_int[2] == 1:
                            start = dt(start_list_int[0], m, first_last_day_of_the_month[0])
                            stop = dt(stop_list_int[0], m + 1, 1)
                            # stop = dt(stop_list_int[0], stop_list_int[1], stop_list_int[2])
                        else:
                            start = dt(start_list_int[0], m, first_last_day_of_the_month[0])
                            stop = dt(stop_list_int[0], stop_list_int[1], stop_list_int[2])
                    filename = download_part(user_hisparc_station_id, start, stop)
                    downloaded_data_files.append(filename)

    else:
        print 'Error in date input'
        print 'Either your stop date is before your start date or you entered a date from before the start of HiSPARC'

    print 4 * "\a"
    return downloaded_data_files


def download_part(user_hisparc_station_id, start, stop):

    """ Download HiSPARC data from start till stop

    """
    hisp_station = int(user_hisparc_station_id)
    tree = '/s' + user_hisparc_station_id
    path = 'data.root.s' + user_hisparc_station_id
    filename = 'data_s%d_%s_%s.h5' % (user_hisparc_station_id,
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
