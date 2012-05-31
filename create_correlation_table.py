from tables import openFile, IsDescription, Float64Col, Int16Col
from scipy import array
import numpy as np
from get_number_of_plates import get_number_of_plates


def create_correlation_table(plot_variable1,plot_variable2, values1, values2,seconds):

    if len(values2) == len(values1):
        print ''
        print 'Creating new table...'
        print ''

        number_of_plates1 = 0
        number_of_plates2 = 0

        if plot_variable1[0][0] == 'pulseheights' or plot_variable1[0][0] == 'integrals' or plot_variable2[0][0] == 'pulseheights' or plot_variable2[0][0] == 'integrals':
            if plot_variable1[0][0] == 'pulseheights' or plot_variable1[0][0] == 'integrals':
                number_of_plates1 = get_number_of_plates(values1[0])
            if plot_variable2[0][0] == 'pulseheights' or plot_variable2[0][0] == 'integrals':
                number_of_plates2 = get_number_of_plates(values2[0])

        # declare a class
        class Variable1(IsDescription):
            if number_of_plates1 in range(1,5) and number_of_plates2 in range(1,5):
                variable1 = Float64Col(shape=(number_of_plates1,))
                variable2 = Float64Col(shape=[number_of_plates2,])
            elif number_of_plates1 in range(1,5) and number_of_plates2 not in range(1,5):
                variable1 = Float64Col(shape=(number_of_plates1,))
                variable2 = Float64Col()
            elif number_of_plates1 not in range(1,5) and number_of_plates2 in range(1,5):
                variable1 = Float64Col()
                variable2 = Float64Col(shape=(number_of_plates2,))
            elif number_of_plates1 not in range(1,5) and number_of_plates2 not in range(1,5):
                variable1 = Float64Col()
                variable2 = Float64Col()
            else:
                print 'weird'


        # create filename for correlation table from data filenames
        intermediate1 = plot_variable1[0][1].replace('data_s' + str(plot_variable1[0][2]) + '_', '')
        intermediate2 = intermediate1.partition(' -')
        start_date = intermediate2[0]
        intermediate3 = intermediate2[2][1:]
        end_date = intermediate3.replace('.h5','')

        filename = 'interpolated_table_' + str(plot_variable1[0][0]) + '_station' + str(plot_variable1[0][2]) + '_with_' + str(plot_variable2[0][0]) + '_station' + str(plot_variable2[0][2]) + '_' + start_date + '_' + end_date + '_timeinterval_' + str(seconds) + '.h5'

        # make new table
        data_cor = openFile(filename, 'w')
        group_variable1 = data_cor.createGroup("/", 'correlation')
        table_variable1 = data_cor.createTable(group_variable1, 'table', Variable1)

        # Insert a new particle record
        particle = table_variable1.row

        for i in range(len(values1)):

            particle['variable1'] = values1[i]
            particle['variable2'] = values2[i]
            particle.append()

        table_variable1.flush()

        data_cor.close()
        print 'Done.'
        return filename
    else:
        print 'Your variable lists are not of the same length. Interpolation is necessary.'

"""
plot_variable1 = [('pulseheights', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'events')]
plot_variable2 = [('barometer', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'weather')]
values1 = [[223.06891567, 225.14306157, 251.37563667, 232.49152614], [ 222.83678403, 230.11266675, 252.46212176, 240.34877713], [ 221.93477928, 220.55830496, 252.18763693, 240.20223774], [ 221.6312732,  220.12749912, 251.39484828, 239.72122819], [ 220.85181864, 219.55821876, 245.45944561, 238.99690943], [ 220.78591021, 217.19816959, 242.16822914, 229.78131259], [ 221.1946917,  217.67203598, 241.777909,   229.3671103 ],[ 220.74065915, 247.9401853,  241.41402889, 228.91195226], [ 220.87410269, 254.73319246, 241.74092198, 228.8921862 ], [ 220.55980287, 222.65687533, 241.62508524, 228.94540398]]
values2 = [1022.01842664,1017.68443154,1015.94049896,1016.51496527,1012.48148295,1006.521563, 1006.6486162, 1007.52539461,1011.76778161,1017.13496572]

filename = create_correlation_table(plot_variable1,plot_variable2, values1, values2)
"""
