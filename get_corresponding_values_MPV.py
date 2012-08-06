from scipy import array
import tables
from query_yes_no import query_yes_no
from variable_limits import low_limit, high_limit


def get_corresponding_values_MPV(plot_variable2, times):
    data_sorted = []
    var_list_without_bad_data2 = []

    for i in range(len(plot_variable2)):
        # open datafile
        with tables.openFile(plot_variable2[i][1], 'r') as data:
            # get variable values from data file
            var_string = "data.root.s%s.%s.col('%s')" % (plot_variable2[i][2], plot_variable2[i][3], plot_variable2[i][0])
            var = eval(var_string)

            # get timestamp values corresponding to the variable values from datafile
            ts_string = "data.root.s%s.%s.col('timestamp')" % (plot_variable2[i][2], plot_variable2[i][3])
            ts = eval(ts_string)

        data_sorted.extend(sorted(zip(ts, var))) # one list with timestamps and variable values

    if plot_variable2[0][0] in low_limit:
        bad_data2 = []

        for t2, v2 in data_sorted:
            if v2 >= low_limit[plot_variable2[0][0]] and v2 <= high_limit[plot_variable2[0][0]]:
                var_list_without_bad_data2.append((t2, v2))
            else:
                bad_data2.append((t2, v2))

        if bad_data2:
            print 'Removed %d rows of bad %s data.' % (len(data_sorted) - len(var_list_without_bad_data2), plot_variable2[0][0])
            print_bad_data2 = query_yes_no('Do you want to print the BAD data?')
            if print_bad_data2:
                print bad_data2

    if len(times) <= 1: # a correlation analysis for one datapoint is pointless
        print 'not enough data'
    else: # the plot module gives the center of every time interval. From this the begin- and end-timestamp for every time-interval is calculated
        # times[0] = 1000 s, times[1] = 2000 s, times[2] = 3000 s.

        begin_end_timestamp_list = [times[0] - ((times[1] - times[0]) / 2) + i * (times[1] - times[0]) for i in range(len(times) + 1)]
        #                        = 1000      - (2000 - 1000)/2             + 0 * (2000 - 1000) = 1000 - 500 + 0 = 500 s
        #                        = 1000      - 500                         + 1 * 1000 = 1000 - 500 + 1000 = 1500 s
        #                        = 1000      - 500                         + 2 * 1000 = 1000 - 500 + 2000 = 2500 s

    # for every timeinterval the variable values are brought together

    data_list_to_calculate_mean = []

    for i in range(len(times)):
        mean_data_list_int = []
        for ts, var in var_list_without_bad_data2:
            if ts > begin_end_timestamp_list[i] and ts < begin_end_timestamp_list[i + 1]:
                mean_data_list_int.append([ts, var])

        data_list_to_calculate_mean.append(array(mean_data_list_int))
    # for every time interval the mean of the variable is calculated

    mean_variable_list = []

    for j in data_list_to_calculate_mean:
        if len(j.shape) == 2:
            if len(j[0]):
                var_list = j[:, 1]
                mean = sum(var_list) / len(var_list)
                mean_variable_list.append(mean)
            else:
                print 'No data for this time interval: list is empty.'
        elif len(j.shape) == 1:
            print 'No data for this time interval: list is empty.'
            print 'weird'
    mean_variable_list = array(mean_variable_list)

    return mean_variable_list

"""
#plot_variable1 = [('pulseheights', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'events')]
#values = array([[223.06891567, 225.14306157, 251.37563667, 232.49152614], [ 222.83678403, 230.11266675, 252.46212176, 240.34877713], [ 221.93477928, 220.55830496, 252.18763693, 240.20223774], [ 221.6312732,  220.12749912, 251.39484828, 239.72122819], [ 220.85181864, 219.55821876, 245.45944561, 238.99690943], [ 220.78591021, 217.19816959, 242.16822914, 229.78131259], [ 221.1946917,  217.67203598, 241.777909,   229.3671103 ],[ 220.74065915, 247.9401853,  241.41402889, 228.91195226], [ 220.87410269, 254.73319246, 241.74092198, 228.8921862 ], [ 220.55980287, 222.65687533, 241.62508524, 228.94540398]])

plot_variable2 = [('barometer', 'data_s501_2011,12,1 - 2011,12,23.h5', '501', 'weather')]
#plot_variable2 = [('barometer', 'data_s501_2011,12,7 - 2011,12,8.h5', '501', 'weather'), ('barometer', 'data_s501_2011,12,8 - 2011,12,9.h5', '501', 'weather')]

times = array([1323237603, 1323280803, 1323324003, 1323367203])

mean_variable_list = get_corresponding_values(plot_variable2,times)
"""
