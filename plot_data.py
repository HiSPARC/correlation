import matplotlib.pyplot as plt
import tables
from datetime import datetime
from scipy import array

import question
from query_yes_no import query_yes_no
from split_data_file_in_parts import split_data_file_in_parts
from find_MPV_pulseheights import find_MPV_pulseheights
from find_MPV_integrals import find_MPV_integrals
from create_correlation_table import create_correlation_table
from get_number_of_plates import get_number_of_plates
from units import units


def plot(x, y):
    plt.plot(x, y)
#    locs, labels = plt.xticks()
#    plt.xticks(locs, map(lambda x: "%g" % x, locs))
#    locs, labels = plt.yticks()
#    plt.yticks(locs, map(lambda x: "%g" % x, locs))
    plt.grid(True)
    plt.show()


def plot_data(plot_variable):
    MPV = False

    # These variables are stored per plate, so we have 2 or 4 values
    # for one event instead of just 1.

    if plot_variable[0][0] in ('pulseheights', 'integrals',
                               'baseline', 'std_dev', "n_peaks"):

        if plot_variable[0][0] in ('pulseheights', 'integrals'):
            MPV = query_yes_no('Do you want to PLOT the MPV (Most probable value) of the %s?' % plot_variable[0][0])

        if MPV == True:
            print ''
            interval = question.digit("Select the time interval (in seconds) over which the MPV values must be calculated ( e.g. for a day enter '86400' ): ")
            seconds = int(interval)
            variable_parts, time, number_of_plates = split_data_file_in_parts(plot_variable, seconds)
            #e.g. variable_parts = [[p1, p2...pn], [p1, p2...pn], ....]
            # time [t1, t2...tn] times are timestamps in the middle of every time interval

            if plot_variable[0][0] == 'pulseheights':
                MPV_list, number_of_plates, times = find_MPV_pulseheights(variable_parts, plot_variable, time, number_of_plates)

                #times = array(time) necessary?

                times_dates = [datetime.fromtimestamp(x) for x in times]

                plot_variable1 = [('pulseheights', plot_variable[0][1], plot_variable[0][2], 'events')]
                plot_variable2 = [('time', plot_variable[0][1], plot_variable[0][2], 'events')]

                values1 = MPV_list
                values2 = time

                filename = create_correlation_table(plot_variable1, plot_variable2, values1, values2, seconds)

            elif plot_variable[0][0] == 'integrals':
                MPV_list, number_of_plates = find_MPV_integrals(variable_parts, plot_variable)

            values = array(MPV_list)

            for i in range(number_of_plates):
                y = values[:, i]
                plt.plot(times_dates, y)
            plt.xlabel('time')
            plt.ylabel('%s (%s)' % (plot_variable[0][0], units[plot_variable[0][0]]))

            # create filename for correlation table from data filenames
            intermediate1 = plot_variable[0][1].replace('data_s%s_' % str(plot_variable[0][2]), '')
            intermediate2 = intermediate1.partition('_')
            start_date = intermediate2[0]

            intermediate1b = plot_variable[-1][1].replace('data_s%s_' % str(plot_variable[-1][2]), '')
            intermediate2b = intermediate1b.partition('_')
            intermediate3b = intermediate2b[2][1:]
            end_date = intermediate3b.replace('.h5', '')

            fname = ('MPV_%s_s%s_%s-%s_timeinterval_%d_seconds.png' %
                     (plot_variable[0][0], plot_variable[0][2], start_date, end_date, seconds))
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
                with tables.openFile(plot_variable[i][1], 'r') as data:
                    tree_time = "data.root.s%s.%s.col('timestamp')" % (plot_variable[i][2], plot_variable[i][3])
                    time = eval(tree_time)

                    tree_variable = "data.root.s%s.%s.col('%s')" % (plot_variable[i][2], plot_variable[i][3], plot_variable[i][0])
                    variable = eval(tree_variable)

                time_list.extend(time)

                number_of_plates = get_number_of_plates(variable[0])

                plate1.extend(list(variable[:, 0]))
                plate2.extend(list(variable[:, 1]))
                if number_of_plates == 4:
                    plate3.extend(list(variable[:, 2]))
                    plate4.extend(list(variable[:, 3]))

            dat_sorted1 = array(sorted(zip(time_list, plate1)))
            dat_sorted2 = array(sorted(zip(time_list, plate2)))
            if number_of_plates == 4:
                dat_sorted3 = array(sorted(zip(time_list, plate3)))
                dat_sorted4 = array(sorted(zip(time_list, plate4)))

            print ''
            print 'Your file(s) contain(s) data from ' + str(datetime.fromtimestamp(dat_sorted1[0][0])) + ' until ' + str(datetime.fromtimestamp(dat_sorted1[-1][0]))
            print ''
            whole = query_yes_no('Do you want to PLOT this whole time interval')

            if whole == True:
                times = dat_sorted1[:, 0]
                x = [datetime.fromtimestamp(i) for i in times]

                y = dat_sorted1[:, 1]
                plt.plot(x, y)
                y = dat_sorted2[:, 1]
                plt.plot(x, y)

                if number_of_plates == 4:
                    y = dat_sorted3[:, 1]
                    plt.plot(x, y)
                    y = dat_sorted4[:, 1]
                    plt.plot(x, y)
                    values = array(zip(dat_sorted1[:, 1], dat_sorted2[:, 1],
                                       dat_sorted3[:, 1], dat_sorted4[:, 1]))
                else:
                    values = array(zip(dat_sorted1[:, 1], dat_sorted2[:, 1]))

                plt.ylabel('%s (%s)' % (plot_variable[0][0], units[plot_variable[0][0]]))

                plt.grid(True)
                plt.show()

                returntype = 'whole'

            elif whole == False:

                x_lim_low = 2
                x_lim_up = 2

                while True:

                    start = datetime.fromtimestamp(dat_sorted1[0][0])

                    print ''
                    print 'Start time: ' + str(start)
                    print 'Seconds in interval: ' + str(dat_sorted1[-1][0] - dat_sorted1[0][0])
                    print ''
                    print 'First you are going to enter the LOWER time limit.'
                    while True:
                        x_lim_low = question.digit('Enter the number of seconds after the start time shown above ( e.g. input "3600" means x_begin = timestamp + 3600 s ): ')
                        x_lim_low = int(x_lim_low)
                        if dat_sorted1[0][0] + x_lim_low <= dat_sorted1[-1][0]:
                            break
                        else:
                            print "Oops! Your lower time limit lies beyond your data set. Try again."
                    print ''
                    print 'Now you are going to enter the UPPER time limit.'
                    while True:
                        x_lim_up = question.digit('Enter the number of seconds after the start time shown above ( e.g. input "86400" means x_end = timestamp + 86400 s ): ')
                        x_lim_up = int(x_lim_up)
                        if x_lim_up > x_lim_low and dat_sorted1[0][0] + x_lim_up <= dat_sorted1[-1][0]:
                            break
                        elif x_lim_up <= x_lim_low:
                            print "Oops! The upper time limit less than or equal to the lower time limit. Try again."
                        elif dat_sorted1[0][0] + x_lim_up > dat_sorted1[-1][0]:
                            print "Oops! Your upper time limit lies beyond your data set. Try again."

                    plot_list1 = array([[t, v] for t, v in dat_sorted1 if dat_sorted1[0][0] + x_lim_low < t < dat_sorted1[0][0] + x_lim_up])
                    plot_list2 = array([[t, v] for t, v in dat_sorted2 if dat_sorted2[0][0] + x_lim_low < t < dat_sorted2[0][0] + x_lim_up])
                    if number_of_plates == 4:
                        plot_list3 = array([[t, v] for t, v in dat_sorted3 if dat_sorted3[0][0] + x_lim_low < t < dat_sorted3[0][0] + x_lim_up])
                        plot_list4 = array([[t, v] for t, v in dat_sorted4 if dat_sorted4[0][0] + x_lim_low < t < dat_sorted4[0][0] + x_lim_up])
                        values = array(zip(plot_list1[:, 1], plot_list2[:, 1],
                                           plot_list3[:, 1], plot_list4[:, 1]))
                    else:
                        values = array(zip(plot_list1[:, 1], plot_list2[:, 1]))

                    times = plot_list1[:, 0]
                    x = [datetime.fromtimestamp(i) for i in times]

                    plt.plot(x, plot_list1[:, 1])
                    plt.plot(x, plot_list2[:, 1])
                    if number_of_plates == 4:
                        plt.plot(x, plot_list3[:, 1])
                        plt.plot(x, plot_list4[:, 1])

                    plt.ylabel('%s (%s)' % (plot_variable[0][0], units[plot_variable[0][0]]))

                    returntype = 'part'
                    plt.show()

                    again = query_yes_no('Do you want to plot again with different values for the UPPER and LOWER time?')
                    if again != True:
                        break

    else:
        variable_list = []
        time_list = []

        for i in range(len(plot_variable)):
            with tables.openFile(plot_variable[i][1], 'r') as data:
                tree_time = "data.root.s%s.%s.col('timestamp')" % (plot_variable[i][2], plot_variable[i][3])
                time = eval(tree_time)

                tree_variable = "data.root.s%s.%s.col('%s')" % (plot_variable[i][2], plot_variable[i][3], plot_variable[i][0])
                variable = eval(tree_variable)

            time_list.extend(time)
            variable_list.extend(variable)

        dat_sorted = array(sorted(zip(time_list, variable_list)))

        print ''
        print 'Your file(s) contain(s) data from %s until %s' % (str(datetime.fromtimestamp(dat_sorted[0][0])), str(datetime.fromtimestamp(dat_sorted[-1][0])))
        print ''
        whole = query_yes_no('Do you want to PLOT this whole time interval?')

        if whole == True:
            times = dat_sorted[:, 0]
            x = [datetime.fromtimestamp(i) for i in times]

            dat_sorted = array(dat_sorted)
            values = dat_sorted[:, 1]
            plt.plot(x, values)

            plt.ylabel('%s (%s)' % (plot_variable[0][0], units[plot_variable[0][0]]))
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
                print 'Seconds in interval: ' + str(dat_sorted[-1][0] - dat_sorted[0][0])
                print ''
                print 'First you are going to enter the LOWER time limit.'
                while True:
                    x_lim_low = question.digit('Enter the number of seconds after the start time shown above ( e.g. input "3600" means x_begin = timestamp + 3600 s ): ')
                    x_lim_low = int(x_lim_low)
                    if dat_sorted[0][0] + x_lim_low <= dat_sorted[-1][0]:
                        break
                    else:
                        print "Oops! Your lower time limit lies beyond your data set. Try again."
                print ''
                print 'Now you are going to enter the UPPER time limit.'
                while True:
                    x_lim_up = question.digit('Enter the number of seconds after the start time shown above ( e.g. input "86400" means x_end = timestamp + 86400 s ): ')
                    x_lim_up = int(x_lim_up)
                    if x_lim_up > x_lim_low and dat_sorted[0][0] + x_lim_up <= dat_sorted[-1][0]:
                        break
                    elif x_lim_up <= x_lim_low:
                        print "Oops! The upper time limit less than or equal to the lower time limit. Try again."
                    elif dat_sorted[0][0] + x_lim_up > dat_sorted[-1][0]:
                        print "Oops! Your upper time limit lies beyond your data set. Try again."

                plot_list = []
                # e.g. dat_sorted = (timestamp, variable)

                for t, v in dat_sorted:
                    if t > dat_sorted[0][0] + x_lim_low and t < dat_sorted[0][0] + x_lim_up:
                         plot_list.append([t, v])

                plot_list = array(plot_list)

                times = plot_list[:, 0]
                values = plot_list[:, 1]

                x = [datetime.fromtimestamp(i) for i in times]

                plt.plot(x, values)
                plt.ylabel('%s (%s)' % (plot_variable[0][0], units[plot_variable[0][0]]))
                plt.grid(True)
                plt.show()
                returntype = 'part'

                again = query_yes_no('Do you want to plot again with a different time limits?')
                if again != True:
                    break

    return values, times, returntype

if __name__ == "__main__":
    plot_data([('n_peaks', 'data_s501_20120712_20120715.h5', '501', 'events')])
