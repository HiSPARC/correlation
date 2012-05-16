import matplotlib.pyplot as plt
import tables
from datetime import datetime
from query_yes_no import query_yes_no
from question_is_digit import question_is_digit
from scipy import array
from split_data_file_in_parts import split_data_file_in_parts
from find_MPV_pulseheights2 import find_MPV_pulseheights
from find_MPV_integrals import find_MPV_integrals
from create_correlation_table import create_correlation_table

units = dict(event_id = '' , timestamp = 'seconds', temp_inside = 'degrees Celcius', temp_outside = 'degrees Celcius', humidity_inside = '%', humidity_outside = '%', barometer = 'hectoPascal', wind_dir = 'degrees', wind_speed = 'm/s', solar_rad = 'Watt/m^2', uv = '', evapotranspiration = 'millimetre', rain_rate = 'millimetre/hour', heat_index = 'degrees Celcius', dew_point = 'degrees Celcius', wind_chill = 'degrees Celcius', nanoseconds = 'nanoseconds', ext_timestamp = 'nanoseconds', data_reduction = '', trigger_pattern = '', baseline = 'ADC counts', std_dev = 'ADC counts', n_peaks = '', pulseheights = 'ADC counts', integrals = 'ADC counts nanonseconds', traces = '', event_rate = 'Hz')

def plot(x,y):
    plt.plot(x,y)
    # xticks
    """
    locs,labels = plt.xticks()
    plt.xticks(locs, map(lambda x: "%g" % x, locs))

    # ytikcs
    locs,labels = plt.yticks()
    plt.yticks(locs, map(lambda x: "%g" % x, locs))
    """
    plt.grid(True)
    plt.show()

def plot_data(plot_variable):

    MPV = False

    if plot_variable[0][0] == 'pulseheights' or plot_variable[0][0] == 'integrals':
        print ''
        MPV = query_yes_no('Do you want to PLOT the MPV value of the ' + plot_variable[0][0] + '? ')
        if MPV == True:

            print ''
            interval = question_is_digit("Select the time interval (in seconds) over which the MPV value must be calculated. ( e.g. for a day you enter '86400' ) " )
            seconds = int(interval)
            variable_parts, time, number_of_plates = split_data_file_in_parts(plot_variable,seconds)
            #e.g. variable_parts = [[p1,p2...pn], [p1,p2...pn],....]
            # time [t1,t2,...tn] times are timestamps in the middle of every time interval



            if plot_variable[0][0] == 'pulseheights':
                MPV_list, number_of_plates,timing = find_MPV_pulseheights(variable_parts,plot_variable,time, number_of_plates)

                #times = array(time) necessary?

                times_dates = [datetime.fromtimestamp(x) for x in timing]
                time_interval_array = array(times_dates)


                plot_variable1 = [('pulseheights', plot_variable[0][1], plot_variable[0][2], 'events')]
                plot_variable2 = [('time', plot_variable[0][1], plot_variable[0][2], 'events')]
                values1 = MPV_list

                values2 = time

                #values1 = [[223.06891567, 225.14306157, 251.37563667, 232.49152614], [ 222.83678403, 230.11266675, 252.46212176, 240.34877713], [ 221.93477928, 220.55830496, 252.18763693, 240.20223774], [ 221.6312732,  220.12749912, 251.39484828, 239.72122819], [ 220.85181864, 219.55821876, 245.45944561, 238.99690943], [ 220.78591021, 217.19816959, 242.16822914, 229.78131259], [ 221.1946917,  217.67203598, 241.777909,   229.3671103 ],[ 220.74065915, 247.9401853,  241.41402889, 228.91195226], [ 220.87410269, 254.73319246, 241.74092198, 228.8921862 ], [ 220.55980287, 222.65687533, 241.62508524, 228.94540398]]
                #values2 = [1022.01842664,1017.68443154,1015.94049896,1016.51496527,1012.48148295,1006.521563, 1006.6486162, 1007.52539461,1011.76778161,1017.13496572]

                filename = create_correlation_table(plot_variable1,plot_variable2, values1, values2,seconds)



            elif plot_variable[0][0] == 'integrals':
                MPV_list, number_of_plates = find_MPV_integrals(variable_parts,plot_variable)
            else:
                print 'problem'



            values = array(MPV_list)


            for i in range(number_of_plates):
                y = values[:,i]

                plt.plot(time_interval_array,y)
                plt.xlabel('time')
                plt.ylabel(plot_variable[0][0] + ' (' + units[plot_variable[0][0]] + ')')

            # create filename for correlation table from data filenames
            intermediate1 = plot_variable[0][1].replace('data_s' + str(plot_variable[0][2]) + '_', '')
            intermediate2 = intermediate1.partition(' -')
            start_date = intermediate2[0]

            intermediate1b = plot_variable[-1][1].replace('data_s' + str(plot_variable[-1][2]) + '_', '')
            intermediate2b = intermediate1b.partition(' -')
            intermediate3b = intermediate2b[2][1:]
            end_date = intermediate3b.replace('.h5','')

            fname = 'MPV_'+ plot_variable[0][0] + '_station' + plot_variable[0][2] + '_' + start_date + '-' + end_date + '_'+ 'timeinterval_' + str(seconds) + '_seconds' +  '.png'
            plt.savefig(fname)
            plt.show()

            returntype = 'MPV'

        else:

            time_list = []

            plate1 = []
            plate2 = []
            plate3 = []
            plate4 = []
            number_of_plates = 0

            for i in range(len(plot_variable)):
                data = tables.openFile(plot_variable[i][1],'r')

                tree_variable = 'data.root.s' + plot_variable[i][2] + '.' + plot_variable[i][3] + "[:]['" + plot_variable[i][0] + "']"
                variable = eval(tree_variable)

                tree_time = 'data.root.s' + plot_variable[i][2] + '.' + plot_variable[i][3] + "[:]['timestamp']"
                time = eval(tree_time)
                data.close()

                time_list.extend(time)


                check = variable[0]
                plate_list = []
                for val in check:
                    if val == -1:
                        pass
                    else:
                        plate_list.append(val)
                number_of_plates = len(plate_list)

                if number_of_plates == 2:
                    plate1.extend(list(variable[:,0]))
                    plate2.extend(list(variable[:,1]))
                elif number_of_plates == 4:
                    plate1.extend(list(variable[:,0]))
                    plate2.extend(list(variable[:,1]))
                    plate3.extend(list(variable[:,2]))
                    plate4.extend(list(variable[:,3]))
                else:
                    print 'problem'

            if number_of_plates == 2:
                dat_sorted1 = array(sorted(zip(time_list, plate1)))
                dat_sorted2 = array(sorted(zip(time_list, plate2)))
            elif number_of_plates == 4:
                dat_sorted1 = array(sorted(zip(time_list, plate1)))
                dat_sorted2 = array(sorted(zip(time_list, plate2)))
                dat_sorted3 = array(sorted(zip(time_list, plate3)))
                dat_sorted4 = array(sorted(zip(time_list, plate4)))
            else:
                print 'problem'
            print ''
            print 'Your file(s) contain(s) data from ' + str(datetime.fromtimestamp(dat_sorted1[0][0])) + ' until ' + str(datetime.fromtimestamp(dat_sorted1[-1][0]))
            print ''
            whole = query_yes_no('Do you want to PLOT this whole time interval')

            if whole == True:
                x = dat_sorted1[:,0]
                times = x
                x = [datetime.fromtimestamp(i) for i in x]
                y = dat_sorted1[:,1]
                plt.plot(x,y)
                y = dat_sorted2[:,1]
                plt.plot(x,y)
                plt.ylabel(plot_variable[0][0] + ' (' + units[plot_variable[0][0]] + ')')

                values = array(zip(dat_sorted1[:,1],dat_sorted2[:,1]))

                if number_of_plates == 4:
                    y = dat_sorted3[:,1]
                    plt.plot(x,y)
                    y = dat_sorted4[:,1]
                    plt.plot(x,y)
                    values = array(zip(dat_sorted1[:,1],dat_sorted2[:,1],dat_sorted3[:,1],dat_sorted4[:,1]))

                plt.grid(True)
                plt.show()

                returntype = 'whole'

            elif whole == False:

                x_lim_low = 2
                x_lim_up = 2

                while True:

                    start = datetime.fromtimestamp(dat_sorted1[0][0])
                    print ''
                    print 'Start time = ' + str(start)
                    print 'You are going to enter the LOWER time value.'
                    print ''
                    x_lim_low = question_is_digit('Enter the number of seconds after this timestamp shown above ( e.g. input "3600" means x_begin = timestamp + 3600 s ): ')
                    x_lim_low = int(x_lim_low)
                    print ''
                    print 'You are going to enter the UPPER time value.'
                    print ''
                    while True:
                        x_lim_up = question_is_digit('Enter the number of seconds after the timestamp shown above ( e.g. input "86400" means x_end = timestamp + 86400 s ): ')
                        x_lim_up = int(x_lim_up)
                        if x_lim_up > x_lim_low and dat_sorted1[0][0] + x_lim_up <= dat_sorted1[-1][0]:
                            break
                        elif x_lim_up < x_lim_low:
                            print "Oops! Your lower time limit is larger than your upper time limit. Try again."
                        elif x_lim_up == x_lim_low:
                            print "Oops! Your lower time limit equals your upper time limit. Try again."
                        if dat_sorted1[0][0] + x_lim_up > dat_sorted1[-1][0]:
                            print "Oops! Your upper time limit lies beyond your data set. Try again."
                    plot_list1 = []
                    plot_list2 = []
                    plot_list3 = []
                    plot_list4 = []

                    for t,v in dat_sorted1:
                        if t > dat_sorted1[0][0] +  x_lim_low and t < dat_sorted1[0][0] + x_lim_up:
                             plot_list1.append([t,v])

                    plot_list1 = array(plot_list1)

                    for t,v in dat_sorted2:
                        if t > dat_sorted2[0][0] +  x_lim_low and t < dat_sorted2[0][0] + x_lim_up:
                             plot_list2.append([t,v])

                    plot_list2 = array(plot_list2)

                    values = array(zip(plot_list1[:,1],plot_list2[:,1]))

                    if number_of_plates == 4:
                        for t,v in dat_sorted3:
                            if t > dat_sorted3[0][0] +  x_lim_low and t < dat_sorted3[0][0] + x_lim_up:
                                 plot_list3.append([t,v])

                        plot_list3 = array(plot_list3)

                        for t,v in dat_sorted4:
                            if t > dat_sorted4[0][0] +  x_lim_low and t < dat_sorted4[0][0] + x_lim_up:
                                 plot_list4.append([t,v])

                        plot_list4 = array(plot_list4)

                        values = array(zip(plot_list1[:,1],plot_list2[:,1],plot_list3[:,1],plot_list4[:,1]))

                    times = plot_list1[:,0]
                    x = [datetime.fromtimestamp(i) for i in times]

                    plt.plot(x,plot_list1[:,1])
                    plt.plot(x,plot_list2[:,1])
                    plt.ylabel(plot_variable[0][0] + ' (' + units[plot_variable[0][0]] + ')')

                    returntype = 'part'

                    if number_of_plates == 4:
                        plt.plot(x,plot_list3[:,1])
                        plt.plot(x,plot_list4[:,1])
                    plt.show()

                    again = query_yes_no('Do you want to plot again with different values for the UPPER and LOWER time?')
                    if again != True:
                        break

    else:
        timing = 0
        pass
    if plot_variable[0][0] != 'pulseheights' and plot_variable[0][0] != 'integrals':
        variable_list = []
        time_list = []

        for i in range(len(plot_variable)):
            data = tables.openFile(plot_variable[i][1],'r')

            tree_variable = 'data.root.s' + plot_variable[i][2] + '.' + plot_variable[i][3] + "[:]['" + plot_variable[i][0] + "']"
            variable = eval(tree_variable)

            tree_time = 'data.root.s' + plot_variable[i][2] + '.' + plot_variable[i][3] + "[:]['timestamp']"
            time = eval(tree_time)
            data.close()

            time_list.extend(time)
            variable_list.extend(variable)

        dat_sorted = sorted(zip(time_list, variable_list))

        print ''
        print 'Your file(s) contain(s) data from ' + str(datetime.fromtimestamp(dat_sorted[0][0])) + ' until ' + str(datetime.fromtimestamp(dat_sorted[-1][0]))
        print ''
        whole = query_yes_no('Do you want to PLOT this whole time interval')

        if whole == True:
            dat_sorted = array(dat_sorted)
            values = dat_sorted[:,1]

            times = dat_sorted[:,0]
            x = [datetime.fromtimestamp(i) for i in times]

            plt.plot(x,values)
            plt.ylabel(plot_variable[0][0] + ' (' + units[plot_variable[0][0]] + ')')
            plt.grid(True)
            plt.show()
            returntype = 'whole'

        elif whole == False:

            x_lim_low = 2
            x_lim_up = 2
            plot_list = []

            while True:
                start = datetime.fromtimestamp(dat_sorted[0][0])
                print ''
                print 'Start time = ' + str(start)
                print 'You are going to enter the LOWER time value.'
                print ''
                x_lim_low = question_is_digit('Enter the number of seconds after this timestamp shown above ( e.g. input "3600" means x_begin = timestamp + 3600 s ): ')
                x_lim_low = int(x_lim_low)
                print ''
                print 'You are going to enter the UPPER time value.'
                print ''
                while True:
                    x_lim_up = question_is_digit('Enter the number of seconds after the timestamp shown above ( e.g. input "86400" means x_end = timestamp + 86400 s ): ')
                    x_lim_up = int(x_lim_up)
                    if x_lim_up > x_lim_low and dat_sorted[0][0] + x_lim_up <= dat_sorted[-1][0]:
                        break
                    elif x_lim_up < x_lim_low:
                        print "Oops! Your lower time limit is larger than your upper time limit. Try again."
                    elif x_lim_up == x_lim_low:
                        print "Oops! Your lower time limit equals your upper time limit. Try again."
                    if dat_sorted[0][0] + x_lim_up > dat_sorted[-1][0]:
                        print "Oops! Your upper time limit lies beyond your data set. Try again."

                plot_list = []
                # e.g. dat_sorted = (timestamp, variable)

                for t,v in dat_sorted:
                    if t > dat_sorted[0][0] +  x_lim_low and t < dat_sorted[0][0] + x_lim_up:
                         plot_list.append([t,v])

                plot_list = array(plot_list)

                returntype = 'part'

                timing = plot_list[:,0]
                values = plot_list[:,1]

                x = [datetime.fromtimestamp(i) for i in timing]

                plt.plot(x,plot_list[:,1])
                plt.ylabel(plot_variable[0][0] + ' (' + units[plot_variable[0][0]] + ')')
                plt.grid(True)
                plt.show()

                again = query_yes_no('Do you want to plot again with different values for the UPPER and LOWER time?')
                if again != True:
                    break

    return values, timing, returntype

"""
#plot_variable = [('pulseheights','data_s501_2011,7,21 - 2011,7,22.h5','501','events')] # 4 platen, een dag
plot_variable = [('pulseheights','data_s501_2011,7,15 - 2011,7,17.h5','501','events')] # 4 platen, twee dagen

#plot_variable = [('pulseheights','data_s8001_2011,12,7 - 2011,12,8.h5','8001','events')] #2 platen een dag
#plot_variable = [('pulseheights','data_s8001_2011,12,11 - 2011,12,13.h5','8001','events')] #2 platen twee dagen
#plot_variable = [('event_rate','data_s8001_2011,12,7 - 2011,12,8.h5','8001','events')] #2 platen een dag

values,times,type = plot_data(plot_variable)


print type
"""




