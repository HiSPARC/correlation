from datetime import date
import datetime
from datetime import datetime
import tables
import re
import os
from pylab import *
from hisparc.publicdb import download_data
from remove_dups_hisparcdata import remove_dups
from remove_dups_weatherdata import remove_dups_weatherdata
from question_is_digit import *
from start_end_day_of_the_month import start_end_day_of_the_month
from check_if_weather import check_if_weather



def diff_month(d1, d2): # calculate the number of months within a time interval
    return (d2.year - d1.year)*12 + d2.month - d1.month + 1

def down_data_in_parts(user_hisparc_station_id, user_start_date_data_interval, user_stop_date_data_interval ):

    # find out how many days of data the user wants to download

    # split user input date strings
    start_list = re.split(',',user_start_date_data_interval)
    stop_list = re.split(',',user_stop_date_data_interval)

    # turn the list of strings into integers
    start_list_int = [int(x) for x in start_list]
    stop_list_int = [int(x) for x in stop_list]

    # turn the date list into date objects
    start_date = date(start_list_int[0], start_list_int[1], start_list_int[2])
    end_date = date(stop_list_int[0], stop_list_int[1], stop_list_int[2])

    list_with_downloaded_data_files = [] # make list of filenames with downloaded data

    if start_date <= end_date and end_date <= date.today() and start_date > date(1998,1,1):

        delta = end_date - start_date
        days = delta.days

        if days <= 31: # If the pytable contains more than a month of data it gets too large to handle for my pc

            # create HDF5 filename from the station id
            stop = stop_list[0] + ',' + stop_list[1] + ',' + str(stop_list_int[2])
            filename = 'data_s' + user_hisparc_station_id + '_' + user_start_date_data_interval + ' - ' + stop + '.h5'

            tree = '/s' + user_hisparc_station_id
            # make an integer from the user input for station_id
            hisp_station = int(user_hisparc_station_id)
            # create HDF5 pytable
            data = tables.openFile(filename, 'w')

            download_data(data, tree, station_id=hisp_station,start=datetime.datetime(start_list_int[0], start_list_int[1], start_list_int[2]),end=datetime.datetime(stop_list_int[0], stop_list_int[1], stop_list_int[2]))
            """ end is 'tot' niet 't/m'
            Dus
            start=datetime.datetime(2011, 6, 29),
            end=datetime.datetime(2011, 6, 30)
            Download alleen de data van 29 juni.
            """
            path = 'data.root.s' + user_hisparc_station_id

            print ''
            remove_dups(data, eval(path))
            weather_data_in_file = check_if_weather(data,filename)
            if weather_data_in_file:
                remove_dups_weatherdata(data,eval(path))




            list_with_downloaded_data_files.append(filename) # append to filenames list

            print ''
            print "'" + filename + "'" + ' has downloaded'
            print ''
            print 'You can find it at the location: ' + os.getcwd()
            print ''
            data.close()

        else: # i.e. the time interval spans MORE than 31 days
            check = stop_list_int[1] + stop_list_int[2]

            if start_list_int[0] != stop_list_int[0] and check != 2: # i.e. the timeinterval spans over two years and the stop date is not the first day of the last year (in that case the user intends to download one whole year)

                # make a list of years to loop through
                nyears = range(0, stop_list_int[0] - start_list_int[0]+1) # e.g. [0,1]
                years = [start_list_int[0] + x for x in nyears] # e.g. [2010,2011]

                for i in years: # loop over the years
                    if i == years[0]:  # for the first year of the chosen date interval download first month
                        if start_list_int[1] != 12:
                            # create list with the first and the last day of the month
                            first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], start_list_int[1])

                            # create HDF5 filename inclusing the station ID and the time interval
                            start = str(i) + ',' + str(start_list_int[1]) + ',' + str(start_list_int[2])
                            stop = str(i) + ',' + str(start_list_int[1]+1) + ',' + str(1)
                            filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                            data = tables.openFile(filename, 'w')

                            tree = '/s' + user_hisparc_station_id
                            hisp_station = int(user_hisparc_station_id)

                            download_data(data, tree, station_id=hisp_station,start=datetime.datetime(i, start_list_int[1], start_list_int[2]),end=datetime.datetime(i, start_list_int[1]+1, 1)) # Here we have to add a day becauce the stop date itself is not downloaded

                            path = 'data.root.s' + user_hisparc_station_id

                            print ''
                            remove_dups(data, eval(path))
                            weather_data_in_file = check_if_weather(data,filename)
                            if weather_data_in_file:
                                remove_dups_weatherdata(data,eval(path))


                            list_with_downloaded_data_files.append(filename) # append to filenames list
                            print ''
                            print "'" + filename + "'" + ' has downloaded'
                            print ''
                            print 'You can find it at the location: ' + os.getcwd()
                            print ''
                            data.close()

                        elif start_list_int[1] == 12:

                            # create list with the first and the last day of the month
                            first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], start_list_int[1])

                            # create HDF5 filename inclusing the station ID and the time interval
                            start = str(i) + ',' + str(start_list_int[1]) + ',' + str(start_list_int[2])
                            stop = str(i+1) + ',' + str(1) + ',' + str(1)
                            filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                            data = tables.openFile(filename, 'w')

                            tree = '/s' + user_hisparc_station_id
                            hisp_station = int(user_hisparc_station_id)

                            download_data(data, tree, station_id=hisp_station,
                                          start=datetime.datetime(i, start_list_int[1], start_list_int[2]),
                                          end=datetime.datetime(i+1,1, 1)) # Here we have to add a day becauce the stop date itself is not downloaded

                            path = 'data.root.s' + user_hisparc_station_id

                            print ''
                            remove_dups(data, eval(path))
                            weather_data_in_file = check_if_weather(data,filename)
                            if weather_data_in_file:
                                remove_dups_weatherdata(data,eval(path))



                            list_with_downloaded_data_files.append(filename) # append to filenames list
                            print ''
                            print "'" + filename + "'" + ' has downloaded'
                            print ''
                            print 'You can find it at the location: ' + os.getcwd()
                            print ''
                            data.close()


                        if start_list_int[1] != 12: # download the rest of the months of the first year of the chosen date interval # condition is necessary because if the december is the only month of the first year we are alredy done
                            months = range(start_list_int[1]+1, 13)  # [...12]
                            for j in months:
                                if j != 12:
                                    first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], j)
                                    start = str(start_list_int[0]) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                                    stop = str(start_list_int[0]) + ',' + str(j+1) + ',' + str(1)
                                    filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                                    data = tables.openFile(filename, 'w')
                                    tree = '/s' + user_hisparc_station_id
                                    hisp_station = int(user_hisparc_station_id)

                                    download_data(data, tree, station_id=hisp_station,start=datetime.datetime(start_list_int[0], j, first_last_day_of_the_month[0]),end=datetime.datetime(i, j+1,1)) # Here we have to add a day becauce the stop date itself is not downloaded

                                    path = 'data.root.s' + user_hisparc_station_id

                                    print ''
                                    remove_dups(data, eval(path))
                                    weather_data_in_file = check_if_weather(data,filename)
                                    if weather_data_in_file:
                                        remove_dups_weatherdata(data,eval(path))


                                    list_with_downloaded_data_files.append(filename) # append to filenames list

                                    print ''
                                    print "'" + filename + "'" + ' has downloaded'
                                    print ''
                                    print 'You can find it at the location: ' + os.getcwd()
                                    print ''
                                    data.close()

                                if j == 12:
                                    first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], j)
                                    start = str(start_list_int[0]) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                                    stop = str(start_list_int[0]+1) + ',' + str(1) + ',' + str(1)
                                    filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                                    data = tables.openFile(filename, 'w')
                                    tree = '/s' + user_hisparc_station_id
                                    hisp_station = int(user_hisparc_station_id)

                                    download_data(data, tree, station_id=hisp_station,start=datetime.datetime(i, j, first_last_day_of_the_month[0]),end=datetime.datetime(i+1,1,1)) # Here we have to add a day becauce the stop date itself is not downloaded

                                    path = 'data.root.s' + user_hisparc_station_id

                                    print ''
                                    remove_dups(data, eval(path))
                                    weather_data_in_file = check_if_weather(data,filename)
                                    if weather_data_in_file:
                                        remove_dups_weatherdata(data,eval(path))



                                    list_with_downloaded_data_files.append(filename) # append to filenames list

                                    print ''
                                    print "'" + filename + "'" + ' has downloaded'
                                    print ''
                                    print 'You can find it at the location: ' + os.getcwd()
                                    print ''
                                    data.close()

                    if i != years[-1] and i != years[0]: # If we are not in the last year and not in the first year of the chosen date interval
                        months = range(1, 13)  # [1, 2, ... 12]
                        for j in months: # Download data for all months
                            if j != 12:
                                first_last_day_of_the_month = start_end_day_of_the_month(i, j)
                                start = str(i) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                                stop = str(i) + ',' + str(j+1) + ',' + str(1)
                                filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                                data = tables.openFile(filename, 'w')
                                tree = '/s' + user_hisparc_station_id
                                hisp_station = int(user_hisparc_station_id)

                                download_data(data, tree, station_id=hisp_station,start=datetime.datetime(i, j, first_last_day_of_the_month[0]),end=datetime.datetime(i, j+1,1)) # Here we have to add a day becauce the stop date itself is not downloaded
                                path = 'data.root.s' + user_hisparc_station_id

                                print ''
                                remove_dups(data, eval(path))
                                weather_data_in_file = check_if_weather(data,filename)
                                if weather_data_in_file:
                                    remove_dups_weatherdata(data,eval(path))



                                list_with_downloaded_data_files.append(filename) # append to filenames list
                                print ''
                                print "'" + filename + "'" + ' has downloaded'
                                print ''
                                print 'You can find it at the location: ' + os.getcwd()
                                print ''
                                data.close()

                            if j == 12:
                                first_last_day_of_the_month = start_end_day_of_the_month(i, j)
                                start = str(i) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                                stop = str(i+1) + ',' + str(1) + ',' + str(1)
                                filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                                data = tables.openFile(filename, 'w')
                                tree = '/s' + user_hisparc_station_id
                                hisp_station = int(user_hisparc_station_id)

                                download_data(data, tree, station_id=hisp_station,start=datetime.datetime(i, j, first_last_day_of_the_month[0]),end=datetime.datetime(i+1,1,1)) # Here we have to add a day becauce the stop date itself is not downloaded
                                path = 'data.root.s' + user_hisparc_station_id

                                print ''
                                remove_dups(data, eval(path))
                                weather_data_in_file = check_if_weather(data,filename)
                                if weather_data_in_file:
                                    remove_dups_weatherdata(data,eval(path))



                                list_with_downloaded_data_files.append(filename) # append to filenames list
                                print ''
                                print "'" + filename + "'" + ' has downloaded'
                                print ''
                                print 'You can find it at the location: ' + os.getcwd()
                                print ''
                                data.close()

                    if i == years[-1]: # If we are in the last year of the chosen date interval
                        # make list of months
                        nmonths = diff_month(date(i,1,1), end_date)
                        months = range(1, nmonths+1)

                        for j in months:
                            if j != months[-1]: # if we are not in the last month of the last year of the chosen date interval
                                first_last_day_of_the_month = start_end_day_of_the_month(i, j)
                                start = str(i) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                                stop = str(i) + ',' + str(j+1) + ',' + str(1)
                                filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                                data = tables.openFile(filename, 'w')
                                tree = '/s' + user_hisparc_station_id
                                hisp_station = int(user_hisparc_station_id)

                                download_data(data, tree, station_id=hisp_station,start=datetime.datetime(i, j, first_last_day_of_the_month[0]),end=datetime.datetime(i, j+1,1))
                                path = 'data.root.s' + user_hisparc_station_id
                                print ''
                                remove_dups(data, eval(path))
                                weather_data_in_file = check_if_weather(data,filename)
                                if weather_data_in_file:
                                    remove_dups_weatherdata(data,eval(path))


                                list_with_downloaded_data_files.append(filename) # append to filenames list

                                print ''
                                print "'" + filename + "'" + ' has downloaded'
                                print ''
                                print 'You can find it at the location: ' + os.getcwd()
                                print ''
                                data.close()

                            if j == months[-1]: # if we are in the last month of the last year of the chosen date interval

                                first_last_day_of_the_month = start_end_day_of_the_month(i, j)
                                start = str(i) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                                stop = str(i) + ',' + str(j) + ',' + str(stop_list_int[2])
                                filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                                data = tables.openFile(filename, 'w')
                                tree = '/s' + user_hisparc_station_id
                                hisp_station = int(user_hisparc_station_id)

                                download_data(data, tree, station_id=hisp_station,start=datetime.datetime(i, j, first_last_day_of_the_month[0]),end=datetime.datetime(i, stop_list_int[1], stop_list_int[2]))

                                path = 'data.root.s' + user_hisparc_station_id
                                print ''
                                remove_dups(data, eval(path))
                                weather_data_in_file = check_if_weather(data,filename)
                                if weather_data_in_file:
                                    remove_dups_weatherdata(data,eval(path))



                                list_with_downloaded_data_files.append(filename) # append to filenames list

                                print ''
                                print "'" + filename + "'" + ' has downloaded'
                                print ''
                                print 'You can find it at the location: ' + os.getcwd()
                                print ''
                                data.close()

            else: # i.e. the time interval is shorter than one year or equal to one year
                if stop_list_int[2] == 1:
                    nmonths = diff_month(start_date, end_date)
                    months = range(start_list_int[1], start_list_int[1] + nmonths - 1)
                else:
                    nmonths = diff_month(start_date, end_date)
                    months = range(start_list_int[1], start_list_int[1]+nmonths)

                for j in months:
                    if j == months[0]:  # finish first month of data
                        first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], j)
                        start = str(start_list_int[0]) + ',' + str(j) + ',' + str(start_list_int[2])
                        stop = str(start_list_int[0]) + ',' + str(j+1) + ',' + str(1)
                        filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                        data = tables.openFile(filename, 'w')
                        tree = '/s' + user_hisparc_station_id
                        hisp_station = int(user_hisparc_station_id)

                        download_data(data, tree, station_id=hisp_station,start=datetime.datetime(start_list_int[0], j, start_list_int[2]),end=datetime.datetime(stop_list_int[0], j+1, 1))

                        path = 'data.root.s' + user_hisparc_station_id
                        print ''
                        remove_dups(data, eval(path))
                        weather_data_in_file = check_if_weather(data,filename)
                        if weather_data_in_file:
                            remove_dups_weatherdata(data,eval(path))



                        list_with_downloaded_data_files.append(filename) # append to filenames list
                        print ''
                        print "'" + filename + "'" + ' has downloaded'
                        print ''
                        print 'You can find it at the location: ' + os.getcwd()
                        print ''
                        data.close()

                    if j != months[0] and j != months[-1]: # if we are NOT downloading the first month of data and also NOT the last month of data
                        first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], j)
                        start = str(start_list_int[0]) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                        stop = str(start_list_int[0]) + ',' + str(j+1) + ',' + str(1)
                        filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                        data = tables.openFile(filename, 'w')
                        tree = '/s' + user_hisparc_station_id
                        hisp_station = int(user_hisparc_station_id)

                        download_data(data, tree, station_id=hisp_station,start=datetime.datetime(start_list_int[0], j, first_last_day_of_the_month[0]),end=datetime.datetime(stop_list_int[0], j+1,1))

                        path = 'data.root.s' + user_hisparc_station_id

                        print ''
                        remove_dups(data, eval(path))
                        weather_data_in_file = check_if_weather(data,filename)
                        if weather_data_in_file:
                            remove_dups_weatherdata(data,eval(path))



                        list_with_downloaded_data_files.append(filename) # append to filenames list
                        print ''
                        print "'" + filename + "'" + ' has downloaded'
                        print ''
                        print 'You can find it at the location: ' + os.getcwd()
                        print ''
                        data.close()

                    if j == months[-1]: # if we are downloading the last month of data
                        if stop_list_int[2] == 1:
                            first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], j)
                            start = str(start_list_int[0]) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                            stop = str(stop_list_int[0]) + ',' + str(j+1) + ',' + str(1)
                            filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                            data = tables.openFile(filename, 'w')
                            tree = '/s' + user_hisparc_station_id
                            hisp_station = int(user_hisparc_station_id)


                            download_data(data, tree, station_id=hisp_station,
                                          start=datetime.datetime(start_list_int[0], j, first_last_day_of_the_month[0]),
                                          end=datetime.datetime(stop_list_int[0], stop_list_int[1], stop_list_int[2]))

                        else:
                            first_last_day_of_the_month = start_end_day_of_the_month(start_list_int[0], j)
                            start = str(start_list_int[0]) + ',' + str(j) + ',' + str(first_last_day_of_the_month[0])
                            stop = str(stop_list_int[0]) + ',' + str(stop_list_int[1]) + ',' + str(stop_list_int[2])
                            filename = 'data_s' + user_hisparc_station_id + '_' + start + ' - ' + stop + '.h5'
                            data = tables.openFile(filename, 'w')
                            tree = '/s' + user_hisparc_station_id
                            hisp_station = int(user_hisparc_station_id)


                            download_data(data, tree, station_id=hisp_station,start=datetime.datetime(start_list_int[0], j, first_last_day_of_the_month[0]),end=datetime.datetime(stop_list_int[0], stop_list_int[1], stop_list_int[2]))

                        path = 'data.root.s' + user_hisparc_station_id

                        print ''
                        remove_dups(data, eval(path))
                        weather_data_in_file = check_if_weather(data,filename)
                        if weather_data_in_file:
                            remove_dups_weatherdata(data,eval(path))



                        list_with_downloaded_data_files.append(filename) # append to filenames list
                        print ''
                        print "'" + filename + "'" + ' has downloaded'
                        print ''
                        print 'You can find it at the location: ' + os.getcwd()
                        print ''
                        data.close()

    else:
        print
        print 'Error time input'
        print 'Your stop date is before your start date or you entered a date from before the start of HiSPARC'
        print


    print 4*'\a'
    return list_with_downloaded_data_files