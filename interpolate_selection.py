from tables import openFile, IsDescription, Float32Col
from scipy import array
import numpy as np

# var1 = array([0.78,0.75,0.80])
# var2 = array([1009,1010,1010])

def interpolate_selection(var1, var2):

    print ''
    print 'Interpolating and creating new table...'
    print ''

    # declare a class
    class Variable1(IsDescription):
        variable1 = Float32Col()
        variable2 = Float32Col()

    """
    intermediate1 = var1[0][1].replace('data_s' + str(var1[0][2]) + '_', '')
    station_id_and_date_interval1 = intermediate1.replace('.h5', '')

    intermediate2 = var1[-1][1].replace('data_', '')
    station_id_and_date_interval2 = intermediate2.replace('.h5', '')

    filename = ('cor_' + str(var1[0][0]) + '_' + str(var1[0][2]) + '_' +
               str(var2[0][0]) + '_' + str(var2[0][2]) + '_' +
               station_id_and_date_interval1 + '_' +
               station_id_and_date_interval2 + '.h5')
    """

    filename = 'cor_test.h5'

    # make new table
    data_cor = openFile(filename, 'w')
    group_variable1 = data_cor.createGroup("/", 'correlation')
    table_variable1 = data_cor.createTable(group_variable1, 'table', Variable1)

    # Insert a new particle record
    particle = table_variable1.row

    length_var1 = len(var1)
    length_var2 = len(var2)

    if length_var1 != length_var2:

        # Apply linear interpolation
        if length_var1 > length_var2:
            x = var1[:, 0]
            xp = var2[:, 0]
            fp = var2[:, 1]
            result = np.interp(x, xp, fp)

            variable1 = var1[:, 1]
            variable2 = result
            end_length = length_var1

        elif length_var1 < length_var2:
            x = var2[:, 0]
            xp = var1[:, 0]
            fp = var1[:, 1]
            result = np.interp(x, xp, fp)

            variable1 = result
            variable2 = var2[:, 1]
            end_length = length_var2

        for i in range(end_length):
            particle['variable1'] = variable1[i]
            particle['variable2'] = variable2[i]
            particle.append()

        table_variable1.flush()

    else:
        print ''
        'No interpolation necessary'
        print ''

    data_cor.close()
    print 'Done'

    return filename


"""

bar = progressbar.ProgressBar(maxval=20, \
    widgets=[progressbar.Percentage(), progressbar.Bar('=', '[', ']'), ' ', progressbar.ETA()])

var1 = [('event_rate', 'data_s501_2011,5,23 - 2011,5,31.h5', '501', 'events'), ('event_rate', 'data_s501_2011,6,1 - 2011,6,30.h5', '501', 'events'), ('event_rate', 'data_s501_2011,7,1 - 2011,7,31.h5', '501', 'events'), ('event_rate', 'data_s501_2011,8,1 - 2011,8,31.h5', '501', 'events'), ('event_rate', 'data_s501_2011,9,1 - 2011,9,30.h5', '501', 'events'), ('event_rate', 'data_s501_2011,10,1 - 2011,10,15.h5', '501', 'events')]
var2 = [('barometer', 'data_s501_2011,5,23 - 2011,5,31.h5', '501', 'weather'), ('barometer', 'data_s501_2011,6,1 - 2011,6,30.h5', '501', 'weather'), ('barometer', 'data_s501_2011,7,1 - 2011,7,31.h5', '501', 'weather'), ('barometer', 'data_s501_2011,8,1 - 2011,8,31.h5', '501', 'weather'), ('barometer', 'data_s501_2011,9,1 - 2011,9,30.h5', '501', 'weather'), ('barometer', 'data_s501_2011,10,1 - 2011,10,15.h5', '501', 'weather')]

#var1 = [('event_rate', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'events'), ('event_rate', 'data_s501_2011,7,11 - 2011,7,20.h5', '501', 'events')]
#var2 = [('barometer', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'weather'), ('barometer', 'data_s501_2011,7,11 - 2011,7,20.h5', '501', 'weather')]

#var1 = [('event_rate', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'events')]
#var2 = [('barometer', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'weather')]

interpolate(var1,var2)
"""
