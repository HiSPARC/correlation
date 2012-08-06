from tables import openFile, IsDescription, Float64Col, Int16Col
from scipy import array
import numpy as np

from get_number_of_plates import get_number_of_plates


def create_correlation_table(plot_variable1, plot_variable2, values1, values2, seconds):

    if len(values2) == len(values1):
        print ''
        print 'Creating new table...'
        print ''

        number_of_plates1 = 0
        number_of_plates2 = 0

        if plot_variable1[0][0] in ('pulseheights', 'integrals'):
            number_of_plates1 = get_number_of_plates(values1[0])
        if plot_variable2[0][0] in ('pulseheights', 'integrals'):
            number_of_plates2 = get_number_of_plates(values2[0])

        # declare a class
        class Variable1(IsDescription):
            if number_of_plates1 in range(1, 5) and number_of_plates2 in range(1, 5):
                variable1 = Float64Col(shape=(number_of_plates1,))
                variable2 = Float64Col(shape=[number_of_plates2,])
            elif number_of_plates1 in range(1, 5) and number_of_plates2 not in range(1, 5):
                variable1 = Float64Col(shape=(number_of_plates1,))
                variable2 = Float64Col()
            elif number_of_plates1 not in range(1, 5) and number_of_plates2 in range(1, 5):
                variable1 = Float64Col()
                variable2 = Float64Col(shape=(number_of_plates2,))
            elif number_of_plates1 not in range(1, 5) and number_of_plates2 not in range(1, 5):
                variable1 = Float64Col()
                variable2 = Float64Col()
            else:
                print 'weird'

        # create filename for correlation table from data filenames
        intermediate1 = plot_variable1[0][1].replace('data_s%s_' % plot_variable1[0][2], '')
        intermediate2 = intermediate1.partition('_')
        start_date = intermediate2[0]
        intermediate3 = intermediate2[2][1:]
        end_date = intermediate3.replace('.h5', '')

        filename = (('interpolated_table_%s_station%s_with_%s_station%s_%s_%s'
                     '_timeinterval_%d.h5') %
                    (plot_variable1[0][0], plot_variable1[0][2],
                     plot_variable2[0][0], plot_variable2[0][2],
                     start_date, end_date, seconds))

        # make new table
        with openFile(filename, 'w') as data_cor:
            group_variable1 = data_cor.createGroup("/", 'correlation')
            table_variable1 = data_cor.createTable(group_variable1, 'table', Variable1)

            # Insert a new particle record
            particle = table_variable1.row

            for i in range(len(values1)):
                particle['variable1'] = values1[i]
                particle['variable2'] = values2[i]
                particle.append()

            table_variable1.flush()

        print 'Done.'
        return filename
    else:
        print 'Your variable lists are not of the same length. Interpolation is necessary.'
