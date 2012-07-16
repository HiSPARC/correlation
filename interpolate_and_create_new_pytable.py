from sys import exit
from datetime import datetime

from tables import openFile, IsDescription, Float64Col
from scipy import array
import numpy as np
import matplotlib.pyplot as plt

from query_yes_no import query_yes_no
from question_is_digit_plate import question_is_digit_plate

# var1 = ['event_rate', 'filename', 'station_ID', 'kind']
# var2 = ['event_rate', 'filename', 'station_ID', 'kind']


def interpolate(var1,var2):
    low_limit = dict(temp_inside = -200,
                     temp_outside = -200,
                     humidity_inside = 0,
                     humidity_outside = 0,
                     barometer = 700,
                     wind_dir = 0,
                     wind_speed = 0,
                     solar_rad = 0,
                     uv = 0,
                     evapotranspiration = 0,
                     rain_rate = 0,
                     heat_index = -200,
                     dew_point = -200,
                     wind_chill = -200,
                     pulseheights = 0,
                     integrals = 0,
                     event_rate = 0)
    high_limit = dict(temp_inside = 200,
                      temp_outside = 200,
                      humidity_inside = 100,
                      humidity_outside = 100,
                      barometer = 1200,
                      wind_dir = 360,
                      wind_speed = 500,
                      solar_rad = 1500,
                      uv = 50,
                      evapotranspiration = 1000,
                      rain_rate = 1000,
                      heat_index = 200,
                      dew_point = 200,
                      wind_chill = 200,
                      pulseheights = 25000,
                      integrals = 1000000000,
                      event_rate = 3.5)

    print ''
    print 'Interpolating and creating new table...'
    print ''

    # declare a class
    class Variable1(IsDescription):
        variable1 = Float64Col()
        variable2 = Float64Col()

    intermediate1 = var1[0][1].replace('data_s' + str(var1[0][2]) + '_', '')
    intermediate2 = intermediate1.partition(' -')
    start_date = intermediate2[0]
    intermediate3 = intermediate2[2][1:]
    end_date = intermediate3.replace('.h5','')
    filenom = 'interpolated_table_' + str(var1[0][0]) + '_station' + str(var1[0][2]) + '_with_' + str(var2[0][0]) + '_station' + str(var2[0][2]) + '_' + start_date + '_' + end_date + '.h5'

    """
    intermediate1 = var1[0][1].replace('data_s' + str(var1[0][2]) + '_', '')
    station_id_and_date_interval1 = intermediate1.replace('.h5', '')

    intermediate2 = var1[-1][1].replace('data_', '')
    station_id_and_date_interval2 = intermediate2.replace('.h5', '')

    filenom = 'cor_' + str(var1[0][0]) + '_' + str(var1[0][2]) + '_' + str(var2[0][0]) + '_' + str(var2[0][2]) + '_' + station_id_and_date_interval1 + '_' + station_id_and_date_interval2 + '.h5'
    """


    # make new table
    data_cor = openFile(filenom, 'w')
    group_variable1 = data_cor.createGroup("/", 'correlation')
    table_variable1 = data_cor.createTable(group_variable1, 'table', Variable1)

    # Insert a new particle record
    particle = table_variable1.row

    for i in range(len(var1)):
        # open data file 1
        data_var1 = openFile(str(var1[i][1]), 'r')
        # fetch timestamps and variable 1 from station 1

        timestamps_station1 = eval("data_var1.root.s%s.%s.col('timestamp')" % (str(var1[i][2]) , str(var1[i][3])))
        var1_station1 = eval("data_var1.root.s%s.%s.col('%s')" % (str(var1[i][2]), str(var1[i][3]), str(var1[i][0])))
        data_var1.close()
        if len(var1_station1.shape) != 1:
            print 'There are %d plates with an individual %s value.' % (var1_station1.shape[1], str(var1[i][0]))
            plate_number1 = int(question_is_digit_plate("Enter the plate number that you want to you use in your correlation analysis ( e.g. '1' ): ", var1_station1.shape[1]))
            var1_station1 = var1_station1[:,plate_number1-1]
            var1_station1.tolist()
        elif len(var1_station1.shape) == 1:
            var1_station1 = var1_station1.tolist()
        else:
            print 'weird'



        # zip the hisparc time stamps together with the event_rates,
        # sort them on the basis of timestamp value
        variable1_sorted = sorted(zip(timestamps_station1,var1_station1))
        del timestamps_station1, var1_station1

        if var1[i][0] in low_limit:
            var_list_without_bad_data = []
            for t1,v1 in variable1_sorted:
                if v1 >= low_limit[var1[i][0]] and  v1 <= high_limit[var1[i][0]]:
                    var_list_without_bad_data.append((t1,v1))

            if len(variable1_sorted) != len(var_list_without_bad_data):
                print 'Removed %d rows of bad %s data.' % (len(variable1_sorted) - len(var_list_without_bad_data), var1[i][0])
                if len(var_list_without_bad_data) == 0:
                    print 'Exit. In your data file there is no valid %s data' % (var1[i][0])
                    exit()

            variable1_sorted = var_list_without_bad_data
            del var_list_without_bad_data

        length_var1 = len(variable1_sorted)

        # open data file 2
        data_var2 = openFile(str(var2[i][1]), 'r')
        #fetch timestamps and variable2 from station 2
        timestamps_station2 = eval("data_var2.root.s%s.%s.col('timestamp')" % (str(var2[i][2]), str(var2[i][3])))
        var2_station2 = eval("data_var2.root.s%s.%s.col('%s')" % (str(var2[i][2]), str(var2[i][3]), str(var2[i][0])))
        data_var2.close()

        if len(var2_station2.shape) != 1:
            print 'There are %d plates with an individual %s value.' % (var2_station2.shape[1], str(var2[i][0]))
            plate_number1 = int(question_is_digit_plate("Enter the plate number that you want to you use in your correlation analysis ( e.g. '1' ): ", var2_station2.shape[1]))
            var2_station2 = var2_station2[:,plate_number1-1]
            var2_station2.tolist()
        elif len(var2_station2.shape) == 1:
            var2_station2 = var2_station2.tolist()
        else:
            print 'weird'

        # zip the hisparc time stamps together with the event_rates,
        # sort them on the basis of timestamp value
        variable2_sorted = sorted(zip(timestamps_station2,var2_station2))
        del timestamps_station2, var2_station2

        if var2[i][0] in low_limit:
            var_list_without_bad_data2 = []

            for t2,v2 in variable2_sorted:
                if v2 >= low_limit[var2[i][0]] and  v2 <= high_limit[var2[i][0]]:
                    var_list_without_bad_data2.append((t2,v2))

            if len(variable2_sorted) != len(var_list_without_bad_data2):
                print 'Removed %d rows of bad %s data.' % (len(variable2_sorted) - len(var_list_without_bad_data2), var2[i][0])
                if len(var_list_without_bad_data2) == 0:
                    print 'Exit. In your data file there is no valid %s data' % (var2[i][0])
                    exit()
            variable2_sorted = var_list_without_bad_data2
            del var_list_without_bad_data2

        length_var2 = len(variable2_sorted)

        if length_var1 != length_var2:
            #print 'variable2_sorted[:10]',variable2_sorted[:10]
            #print 'variable1_sorted[:10]',variable1_sorted[:10]
            # Apply linear interpolation

            if length_var1 > length_var2 :
                x,variable1 = zip(*variable1_sorted)
                xp,fp = zip(*variable2_sorted)

                result = np.interp(x, xp, fp)
                variable2 = result
                del variable1_sorted, variable2_sorted, result, x, xp, fp

                for i in range(len(variable1)):
                    particle['variable1'] = variable1[i]
                    particle['variable2'] = variable2[i]
                    particle.append()
                del variable1, variable2
                table_variable1.flush()


            elif length_var1 < length_var2:
                xp,fp = zip(*variable1_sorted)
                x,variable2 = zip(*variable2_sorted)

                result = np.interp(x, xp, fp)
                variable1 = result
                del variable1_sorted, variable2_sorted, result, x, xp, fp

                for i in range(len(variable1)):
                    particle['variable1'] = variable1[i]
                    particle['variable2'] = variable2[i]
                    particle.append()
                del variable1, variable2
                table_variable1.flush()


        else:
            print ''
            'No interpolation necessary'
            print ''
            timestamps_station1,var1_station1 = zip(*variable1_sorted)
            del variable1_sorted
            timestamps_station2,var1_station2 = zip(*variable2_sorted)
            del variable2_sorted
            combo_two_vars = zip(timestamps_station1,var1_station1,timestamps_station2,var1_station2)
            del timestamps_station1,var1_station1,timestamps_station2,var1_station2
            combo_new = []
            for combo in combo_two_vars:
                if combo[0] == combo[2]:
                    combo_new.append([combo[1],combo[3]])

            var1,var2 = zip(*combo_new)
            del combo_new
            for i in range(len(var1)):
                particle['variable1'] = var1[i]
                particle['variable2'] = var2[i]
                particle.append()
            del var1, var2
            table_variable1.flush()

    data_cor.close()

    return filenom
"""
import tables
data = tables.openFile('data_s501_2011,7,21 - 2011,7,22.h5','r')

colnames_shower = data.root.s501.events.colnames
index = colnames_shower.index('baseline')
colnames_shower = colnames_shower[index+1:]
colnames_weather = data.root.s501.weather.colnames
data.close()

for var_shower in colnames_shower:
    for var_weather in colnames_weather:
        print ''
        print var_shower, var_weather
        var1 = [('%s' % (var_shower), 'data_s501_2011,7,21 - 2011,7,22.h5', '501', 'events')]
        var2 = [('%s' % (var_weather), 'data_s501_2011,7,21 - 2011,7,22.h5', '501', 'weather')]
        interpolate(var1,var2)

#var1 = [('baseline', 'data_s501_2011,7,21 - 2011,7,22.h5', '501', 'events')]
#var2 = [('event_rate', 'data_s501_2011,7,21 - 2011,7,22.h5', '501', 'events')]

#var1 = [('event_rate', 'data_s501_2011,12,1 - 2011,12,23.h5', '501', 'events')]
#var2 = [('humidity_outside', 'data_s501_2011,12,1 - 2011,12,23.h5', '501', 'weather')]


#var1 = [('event_rate', 'data_s501_2011,5,23 - 2011,6,1.h5', '501', 'events'), ('event_rate', 'data_s501_2011,6,1 - 2011,6,30.h5', '501', 'events'), ('event_rate', 'data_s501_2011,7,1 - 2011,7,31.h5', '501', 'events'), ('event_rate', 'data_s501_2011,8,1 - 2011,8,31.h5', '501', 'events'), ('event_rate', 'data_s501_2011,9,1 - 2011,9,30.h5', '501', 'events'), ('event_rate', 'data_s501_2011,10,1 - 2011,10,15.h5', '501', 'events')]
#var2 = [('barometer', 'data_s501_2011,5,23 - 2011,6,1.h5', '501', 'weather'), ('barometer', 'data_s501_2011,6,1 - 2011,6,30.h5', '501', 'weather'), ('barometer', 'data_s501_2011,7,1 - 2011,7,31.h5', '501', 'weather'), ('barometer', 'data_s501_2011,8,1 - 2011,8,31.h5', '501', 'weather'), ('barometer', 'data_s501_2011,9,1 - 2011,9,30.h5', '501', 'weather'), ('barometer', 'data_s501_2011,10,1 - 2011,10,15.h5', '501', 'weather')]

#var1 = [('event_rate', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'events'), ('event_rate', 'data_s501_2011,7,11 - 2011,7,20.h5', '501', 'events')]
#var2 = [('barometer', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'weather'), ('barometer', 'data_s501_2011,7,11 - 2011,7,20.h5', '501', 'weather')]

#var1 = [('event_rate', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'events')]
#var2 = [('barometer', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'weather')]
"""


