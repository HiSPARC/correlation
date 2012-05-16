from datetime import datetime, date, timedelta
import re
import os
import tables
from pylab import *
from hisparc.publicdb import download_data
import time
from query_yes_no import query_yes_no

def read_list_from_file():

    print ''
    print 'The last check for operational stations was at: ' + time.ctime(os.path.getctime('operational_hisparc_and_weather_station_IDs.txt'))
    print ''



    da = open('operational_hisparc_and_weather_station_IDs.txt','r')


    list = da.readlines() # returns a list. Every item from the list is a string containing a line from the file.

    a = list[0].replace('\n', '') # to remove the newline sign from the first line of the file

    b = a.replace('operational_hisparc_station_IDs = ', '') # remove the text from the first line

    c = list[1].replace('operational_weather_station_IDs = ', '') # remove the text from the second line

    operational_hisparc_station_IDs = eval(b) # creates a list with hisparc station IDs

    operational_weather_station_IDs = eval(c) # creates a list with weather station IDs

    da.close() # close the file

    print '- Currently we have the following HiSPARC stations operational:'
    print operational_hisparc_station_IDs
    print ''
    print '- Currently we have the following WEATHER stations operational:'
    print operational_weather_station_IDs
    print ''


def search_operational_stations():

    if os.path.isfile('operational_hisparc_and_weather_station_IDs.txt'):
        read_list_from_file()
    else:
        print 'You do not have a list with operational stations in your current working directory.'

    update = query_yes_no('Do you want to update/create the list with operational stations? (this can take about 20 minutes) ')
    print ''

    if update == True:

        stationID_list = [20001, 20002, 20003, 401, 402, 7201, 3301, 3302, 3303, 2, 3, 5, 6, 7, 9, 10, 13, 21, 22, 13001, 11001, 7301, 8001, 8002, 8003, 8004, 8005, 8006, 8007, 8099, 7001, 7002, 7003, 4001, 4002, 4003, 4004, 4099, 7401, 201, 202, 40001, 7101, 601, 701, 301, 302, 303, 304, 3001, 3002, 3003, 3099, 3201, 3202, 3203, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 8201, 1, 19, 96, 97, 98, 99, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 10001, 10002, 3401, 8101, 8102, 8103, 8104, 8105, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1099, 2101, 2102, 2103, 30001, 8301, 8302, 8303, 101, 102, 103, 3101, 3102, 3103, 3104]
        #stationID_list = [20001, 501, 502]

        operational_hisparc_station_IDs = []
        operational_weather_station_IDs = []

        yesterday = str(date.today() - timedelta(days=1))
        yest_without_zero = yesterday.replace('-0',',')
        yest_without_hyphen = yest_without_zero.replace('-',',')
        start_list = re.split(',',yest_without_hyphen)
        start_list_int = [int(x) for x in start_list] # turn the list of strings into integers

        today = str(date.today())
        today_without_zero = today.replace('-0',',')
        today_without_hyphen = today_without_zero.replace('-',',')
        stop_list = re.split(',',today_without_hyphen)
        stop_list_int = [int(x) for x in stop_list]

        for i in stationID_list:

            filename = str(i)+'_'+ yesterday + '.h5'
            tree = '/s' + str(i)

            data = tables.openFile(filename, 'w')
            download_data(data, tree, i,
                      start=datetime.datetime(start_list_int[0], start_list_int[1], start_list_int[2]),
                      end=datetime.datetime(stop_list_int[0], stop_list_int[1], stop_list_int[2]))

            data.close()

            data = tables.openFile(filename, 'r')
            table = data.root
            children = table._v_nchildren

            if not children:
                data.close()
                pass
            else:

                folder = 's' + str(i)
                group = 'data.root.' + folder

                if 'events' in eval(group):
                    operational_hisparc_station_IDs.append(i)

                if 'weather' in eval(group):
                    operational_weather_station_IDs.append(i)

                data.close()
            os.remove(filename)

        sorted_hisp_ID = sort(operational_hisparc_station_IDs)
        sorted_weath_ID = sort(operational_weather_station_IDs)

        file = open('operational_hisparc_and_weather_station_IDs.txt','w')
        file.write('operational_hisparc_station_IDs = [')

        for i in range(len(sorted_hisp_ID)):
            if i != range(len(sorted_hisp_ID))[-1]:
                file.write("%s, " % sorted_hisp_ID[i])
            elif i == range(len(sorted_hisp_ID))[-1]:
                file.write("%s" % sorted_hisp_ID[i])
            else:
                print 'problem'

        file.write(']')

        file.write("%s\n" % (''))
        file.write('operational_weather_station_IDs = [')

        for i in range(len(sorted_weath_ID)):
            if i != range(len(sorted_weath_ID))[-1]:
                file.write("%s, " % sorted_weath_ID[i])
            elif i == range(len(sorted_hisp_ID))[-1]:
                file.write("%s" % sorted_weath_IDID[i])
            else:
                print 'problem'

        file.write(']')

        file.close()

        read_list_from_file()








