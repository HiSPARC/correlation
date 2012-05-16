from scipy import array
import tables

def get_corresponding_values_selection(plot_variable2,times):
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
                      uv = 30,
                      evapotranspiration = 1000,
                      rain_rate = 1000,
                      heat_index = 200,
                      dew_point = 200,
                      wind_chill = 200,
                      pulseheights = 25000,
                      integrals = 1000000000,
                      event_rate = 3.5)

    data_sorted = []

    for i in range(len(plot_variable2)):
        # open datafile
        data = tables.openFile(plot_variable2[i][1], 'r')

        # get variable values from data file
        var_string = 'data.root.s' +  plot_variable2[i][2]+ '.' + plot_variable2[i][3] + "[:]['" + plot_variable2[i][0] + "']"
        var = eval(var_string)

        # get timestamp values corresponding to the variable values from datafile
        ts_string = 'data.root.s' +  plot_variable2[i][2]+ '.' + plot_variable2[i][3] + "[:]['timestamp']"
        ts = eval(ts_string)

        data.close()

        data_sorted.extend(sorted(zip(ts,var))) # one list with timestamps and variable values

    if plot_variable2[0][0] in low_limit:
        var_list_without_bad_data2 = []
        bad_data2 = []

        for t2,v2 in data_sorted:
            if v2 > low_limit[plot_variable2[0][0]] and  v2 < high_limit[plot_variable2[0][0]]:
                var_list_without_bad_data2.append((t2,v2))
            else:
                bad_data2.append((t2,v2))

        if bad_data2:
            print 'Removed %d rows of bad %s data.' % (len(data_sorted) - len(var_list_without_bad_data2), plot_variable2[0][0])
            print_bad_data2 = query_yes_no('Do you want to print the BAD data?')
            if print_bad_data2:
                print bad_data2

    # for the specified timeinterval the variable2 values are brought together

    variable2_values = []

    for ts,var in data_sorted:
        if ts > times[0] and ts < times[-1]:
            variable2_values.append([ts,var])

    variable2_values = array(variable2_values)

    return variable2_values

"""
#plot_variable1 = [('pulseheights', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'events')]
#values = array([[223.06891567, 225.14306157, 251.37563667, 232.49152614], [ 222.83678403, 230.11266675, 252.46212176, 240.34877713], [ 221.93477928, 220.55830496, 252.18763693, 240.20223774], [ 221.6312732,  220.12749912, 251.39484828, 239.72122819], [ 220.85181864, 219.55821876, 245.45944561, 238.99690943], [ 220.78591021, 217.19816959, 242.16822914, 229.78131259], [ 221.1946917,  217.67203598, 241.777909,   229.3671103 ],[ 220.74065915, 247.9401853,  241.41402889, 228.91195226], [ 220.87410269, 254.73319246, 241.74092198, 228.8921862 ], [ 220.55980287, 222.65687533, 241.62508524, 228.94540398]])

plot_variable2 = [('barometer', 'data_s501_2011,12,7 - 2011,12,9.h5', '501', 'weather')]
#plot_variable2 = [('barometer', 'data_s501_2011,12,7 - 2011,12,8.h5', '501', 'weather'), ('barometer', 'data_s501_2011,12,8 - 2011,12,9.h5', '501', 'weather')]

times = array([1323216035, 1323216105])

variable2_values = get_corresponding_values_selection(plot_variable2,times)

print variable2_values
"""
