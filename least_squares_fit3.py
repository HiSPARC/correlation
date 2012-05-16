import tables
import numpy as np
import matplotlib.pyplot as plt
from scipy import array
from scipy.stats.stats import chisquare, chisqprob
from query_yes_no import query_yes_no
from downsample import downsample
from datetime import datetime
from question_is_digit_plate import question_is_digit_plate
from get_number_of_plates import get_number_of_plates

# e.g. filename = cor_data_barometer_501_event_rate_502.h5
# e.g. var1 = [('barometer', 'data_s501_2011,6,30 - 2011,6,30.h5', '501', 'weather'), ('barometer', 'data_s501_2011,7,1 - 2011,7,31.h5', '501', 'weather')]
# e.g. var2 = [('event_rate', 'data_s502_2011,6,30 - 2011,6,30.h5', '502', 'events'), ('event_rate', 'data_s502_2011,7,1 - 2011,7,31.h5', '502', 'events')]

def lose_nans(x,y):
    x = [str(i) for i in x]
    y = [str(i) for i in y]

    combo = zip(x,y)

    list = []
    for i in range(len(combo)):
        if combo[i][0] != 'nan' and combo[i][1] != 'nan':
            list.append(combo[i])

    x,y = zip(*list)
    x = [float(i) for i in x]
    x = array(x)
    y = [float(i) for i in y]
    y = array(y)

    return x,y

def get_date_interval_from_file_names(var1, var2):
    first_file = var1[0][1]
    station_ID = var1[0][2]
    inter_string1a = first_file.partition(station_ID + '_')
    inter_string1b = inter_string1a[2].partition(' - ')
    start_date_interval = inter_string1b[0]

    second_file = var1[-1][1]
    inter_string2a = second_file.partition(station_ID + '_')
    inter_string2b = inter_string2a[2].partition(' - ')
    stop_date_interval = inter_string2b[2].replace('.h5', '')

    return start_date_interval, stop_date_interval

def least_squares_fit(filename, variable1,variable2):

    units = dict(event_id = '' , timestamp = 'seconds', temp_inside = 'degrees Celcius', temp_outside = 'degrees Celcius', humidity_inside = '%', humidity_outside = '%', barometer = 'hectoPascal', wind_dir = 'degrees', wind_speed = 'm/s', solar_rad = 'Watt/m^2', uv = '', evapotranspiration = 'millimetre', rain_rate = 'millimetre/hour', heat_index = 'degrees Celcius', dew_point = 'degrees Celcius', wind_chill = 'degrees Celcius', nanoseconds = 'nanoseconds', ext_timestamp = 'nanoseconds', data_reduction = '', trigger_pattern = '', baseline = 'ADC counts', std_dev = 'ADC counts', n_peaks = '', pulseheights = 'ADC counts', integrals = 'ADC counts nanonseconds', traces = '', event_rate = 'Hz')
    # open data file
    data = tables.openFile(filename, 'r')

    # fetch values variable 1 and 2
    variable_1 = data.root.correlation.table[:]['variable1']
    variable_2 = data.root.correlation.table[:]['variable2']
    data.close()

    y_axis = query_yes_no("Do you want to plot '" + variable1[0][0] + "' on the y-axis?")

    if len(variable_1.shape) != 1:
        print 'There are %d plates with an individual %s value.' % (variable_1.shape[1], variable1[0][0])
        plate_number1 = int(question_is_digit_plate("Enter the plate number that you want to you use in your correlation analysis ( e.g. '1' ): ", variable_1.shape[1]))
        variable_1 = variable_1[:,plate_number1-1]

    if len(variable_2.shape) != 1:
        print 'There are %d plates with an individual %s value.' % (variable_2.shape[1], variable2[0][0])
        plate_number2 = int(question_is_digit_plate("Enter the plate number that you want to you use in your correlation analysis ( e.g. '1' ): ", variable_2.shape[1]))
        variable_2 = variable_2[:,plate_number2-1]

    if y_axis == True:
        y = variable_1 # e.g. 'event_rates'
        x = variable_2 # e.g. 'barometric pressure'
        x,y = lose_nans(x,y)

    elif y_axis == False:
        x = variable_1 # e.g. 'event_rates'
        y = variable_2 # e.g. 'barometric pressure'
    else:
        print 'weird'
    del variable_1, variable_2


    # Apply a linear least square fit:
    # a line, ``y = mx + c``, through the data-points:

    # We can rewrite the line equation as ``y = Ap``, where ``A = [[x 1]]``
    # and ``p = [[m], [c]]``.  Now use `lstsq` to solve for `p`:

    A = np.vstack([x, np.ones(len(x))]).T

    a, b = np.linalg.lstsq(A, y)[0]
    del A

    if y_axis == True:
        print ''
        print "The equation for the linear fit line is: ( y = ax + b )   y = " + str(a) + " * x" + " + " + str(b)
        print ''
        print "or     '" + variable1[0][0] + "' = " + str(a) + " * '" + variable2[0][0] + "'" + " + " + str(b)
    elif y_axis == False:
        print ''
        print "The equation for the linear fit line is: ( y = ax + b )   y = " + str(a) + " * x" + " + " + str(b)
        print ''
        print "or     '" + variable2[0][0] + "' = " + str(a) + " * '" + variable1[0][0] + "'" + " + " + str(b)

    # Calculate sample pearson correlation coefficient
    cor_coef = np.corrcoef([x,y])[0,1]

    absolute_cor_coef = abs(cor_coef)
    print ''
    pearson_text = "The Pearson correlation coefficient between '" + variable1[0][0] + "' and '" + variable2[0][0] + "' is : " + str(cor_coef)
    print pearson_text
    print ''

    if absolute_cor_coef >= 0 and absolute_cor_coef < 0.1:
        correlation = 'NO '
    elif absolute_cor_coef >= 0.1 and absolute_cor_coef < 0.3:
        correlation = 'a SMALL '
    elif absolute_cor_coef >= 0.3 and absolute_cor_coef < 0.5:
        correlation = 'a MEDIUM '
    elif absolute_cor_coef >= 0.5 and absolute_cor_coef <= 1:
        correlation = 'a STRONG '

    if cor_coef > 0: #and correlation != 'NO ':
        pos_neg = 'POSITIVE'
    elif cor_coef < 0: #and correlation != 'NO ':
        pos_neg = 'NEGATIVE'
    elif cor_coef == 0:
        pos_neg = ''

    conclusion = "For this sample you have found " + correlation + pos_neg + " correlation between '" + variable1[0][0] + "' and '" + variable2[0][0] + " ."
    print conclusion

    """
    # calculate chi squared
    list_exp = array([a*i + b for i in x])

    begin3 = datetime.now()
    chi2, p = chisquare(y,list_exp)
    end3 = datetime.now()
    print end3 - begin3

    combo = zip(y,list_exp)

    begin = datetime.now()

    ch2 = 0

    for i in combo:
        ch2 = ch2 + (i[0]-i[1]-0.5)**2/i[1]

    print 'chi squared is ', ch2
    end = datetime.now()
    print end - begin



    print ''
    print 'chi squared:', chi2
    print 'associated p-value: ', p
    print ''

    degrees_of_freedom = (len(x) - 1)

    print 'chi squared divided by the number of measurements: ', chi2/degrees_of_freedom

    chi2_prob = chisqprob(chi2,degrees_of_freedom) # probability value associated with the provided chi-square value and degrees of freedom

    print 'probability value associated with the provided chi-square value and degrees of freedom:', chi2_prob
    """

    # Plot the data along with the fitted line:

    if(len(x) > 500000):
        x,y = downsample(x,y)

    plt.plot(x, y, 'o', label='Original data', markersize=1)
    plt.plot(x, a*x + b, 'r', label='Fitted line')

    if y_axis == True:
        plt.ylabel(variable1[0][0] + ' (' + units[variable1[0][0]] + ')')
        plt.xlabel(variable2[0][0] + ' (' + units[variable2[0][0]] + ')')
    elif y_axis == False:
        plt.ylabel(variable2[0][0] + ' (' + units[variable2[0][0]] + ')')
        plt.xlabel(variable1[0][0] + ' (' + units[variable1[0][0]] + ')')

    tit = "Fit line: ( y = ax + b )   y = " + str(a) + " * x" + " + " + str(b)

    plt.legend()
    plt.title(tit)

    start_date_interval, stop_date_interval  = get_date_interval_from_file_names(variable1, variable2)
    inter_filename = filename.replace('.h5', '')
    fname = inter_filename + ' ' + start_date_interval + ' - ' + stop_date_interval

    plt.savefig(fname +".png")
    plt.show()

    fit_info = open(fname + '.txt','w')
    fit_info.write(tit)
    fit_info.write("%s\n" % (''))
    fit_info.write(str(pearson_text))
    fit_info.write("%s\n" % (''))
    fit_info.write(str(conclusion))
    fit_info.close

    """
    # calculate mean y value
    mean_y = sum(y) / len(y)
    print 'mean_y = ', mean_y

    relative_deviation_from_mean_y_list = []
    #relative deviation of the cosmic ray intensity (deltaI/I) from the mean intensity.

    for i in range(len(y)):
        deviation_of_mean_y = y[i] - mean_y
        relative_deviation_from_mean_y = deviation_of_mean_y/mean_y
        relative_deviation_from_mean_y_list.append(relative_deviation_from_mean_y)

    plt.plot(x,relative_deviation_from_mean_y_list,'o',markersize=1)

    plt.ylabel('deltaMPV_p/<MPV_p>')
    plt.xlabel('Outside temperature (degrees Celsius)')

    tit = "Correlation between the Relative deviation of the MPV of the pulseheight (3h intervals) from the mean MPV value with the outside temperature."
    plt.title(tit)

    fname = 'Correlation between relative deviation of the MPV of the pulseheights (3h intervals) from the mean MPV value with T_out'
    plt.savefig(fname +".png")

    plt.show()
    """
    """
    # histogram
    ys = sorted(y)
    bins = int(ys[-1] - ys[0])
    histo = plt.hist(y,bins)
    print histo[0]
    print histo[1]

    plt.show()
    """

"""

#variable1 = [('event_rate', 'data_s501_2011,5,23 - 2011,5,31.h5', '501', 'events'), ('event_rate', 'data_s501_2011,6,1 - 2011,6,30.h5', '501', 'events'), ('event_rate', 'data_s501_2011,7,1 - 2011,7,31.h5', '501', 'events'), ('event_rate', 'data_s501_2011,8,1 - 2011,8,31.h5', '501', 'events'), ('event_rate', 'data_s501_2011,9,1 - 2011,9,30.h5', '501', 'events'), ('event_rate', 'data_s501_2011,10,1 - 2011,10,15.h5', '501', 'events')]
#variable2 = [('barometer', 'data_s501_2011,5,23 - 2011,5,31.h5', '501', 'weather'), ('barometer', 'data_s501_2011,6,1 - 2011,6,30.h5', '501', 'weather'), ('barometer', 'data_s501_2011,7,1 - 2011,7,31.h5', '501', 'weather'), ('barometer', 'data_s501_2011,8,1 - 2011,8,31.h5', '501', 'weather'), ('barometer', 'data_s501_2011,9,1 - 2011,9,30.h5', '501', 'weather'), ('barometer', 'data_s501_2011,10,1 - 2011,10,15.h5', '501', 'weather')]



variable1 = [('pulseheights', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'events')]
variable2 = [('barometer', 'data_s501_2011,7,1 - 2011,7,10.h5', '501', 'weather')]

filename = 'cor_pulseheights_501_barometer_501_2011,7,1 - 2011,7,10_s501_2011,7,1 - 2011,7,10.h5'

least_squares_fit(filename, variable1,variable2)

"""
