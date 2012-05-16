from sys import exit
from pylab import *
from query_yes_no import query_yes_no
import os
from down_data_in_parts_tot import down_data_in_parts
from kind_of_data import kind_of_data
from question_is_digit import question_is_digit
from question_is_digit_and_date import question_is_digit_and_date
from question_is_digit_with_constraint import question_is_digit_with_constraint
from choose_variables_for_correlation import choose_variables_for_correlation
from search_operational_stations import search_operational_stations
from show_downloaded_file_names import show_downloaded_file_names
from interpolate_and_create_new_pytable6 import interpolate
from least_squares_fit3 import least_squares_fit
from get_station_ID_from_filename import get_station_ID_from_filename
from choose_one_variable import choose_one_variable
from plot_data import plot_data
from get_corresponding_values_MPV import get_corresponding_values_MPV
from get_corresponding_values_selection import get_corresponding_values_selection
from create_correlation_table import create_correlation_table
from interpolate_selection import interpolate_selection

print ''
print 'MM     $MM  MMM     MMMM     MMMMMMM         MMM      MMMMMMM         MMMM'
print 'MM     $MM  MMM   MMMMMMMM   MMMMMMMMM8     MMMM      MMMMMMMMMM   ZMMMMMMMM'
print 'MM     $MM       MMM    MMM  MMM    =MM     MMMMM     MM      MM  =MM     MMM'
print 'MM     $MM  MMM   MMMMN      MMM    MMM    MMN MMN    MM     MMM  MMM'
print 'MMMMMMMMMM  MMM     MMMMMM   MMMMMMMMM    MMM   MM    MMMMMMMM    MM8'
print 'MM     $MM  MMM         MMM  MMM          MMMMMMMMM   MM   MMM~   MMM      M'
print 'MM     $MM  MMM  MMM    MMM  MMM         MMM     MM   MM    =MM+   MMM   +MMM'
print 'MM     $MM  MMM   MMMMMMMM   MMM        8MM      MMM  MM      MMO   MMMMMMM='
print ''

print ''
print 'Welcome to HiSPARC download and correlation software!'
print ''
print 'With this program you can download HiSPARC data, plot data and search for a correlation between HiSPARC shower and/or weather variables.'
print ''


download_question = query_yes_no('Do you want to download DATA?')
stations = []
plot_variable1 = []
plot_variable2 = []

if download_question == True:
    show_operational_stations = query_yes_no('Do you want to see a list with operational HiSPARC and WEATHER stations?')
    if show_operational_stations == True:
        search_operational_stations()

    user_hisparc_station_id_1 = question_is_digit('Enter the HiSPARC STATION ID from which you want to download data ( e.g. 501 ): ')
    stations.append(user_hisparc_station_id_1)
    user_start_date_data_interval = question_is_digit_and_date('Enter START date data interval ( e.g. 2011,7,21 ) : ')
    user_stop_date_data_interval = question_is_digit_and_date('Enter STOP date data interval ( e.g. 2011,7,22 ) : ')

    list_file_names_station_1 = down_data_in_parts(user_hisparc_station_id_1, user_start_date_data_interval, user_stop_date_data_interval)

    if list_file_names_station_1:
        pass
    else:
        sys.exit()

    kind_of_data_in_table = kind_of_data(list_file_names_station_1)
    show_downloaded_file_names(kind_of_data_in_table)

    print ''
    down_data_another_station = query_yes_no('Do you want to download data from another station?')

    if down_data_another_station == True:
        user_hisparc_station_id_2 = question_is_digit('Enter the HiSPARC STATION ID from which you want to download data ( e.g. 501 ): ')
        stations.append(user_hisparc_station_id_2)
        print''

        same_dates = query_yes_no('Do you want to use the SAME DATE INTERVAL you entered earlier?')
        if same_dates == True:
            list_file_names_station_2 = down_data_in_parts(user_hisparc_station_id_2, user_start_date_data_interval, user_stop_date_data_interval)

            if list_file_names_station_2:
                pass
            else:
                sys.exit()
            kind_of_data_in_station_2 = kind_of_data(list_file_names_station_2)
            kind_of_data_in_table.extend(kind_of_data_in_station_2)
            show_downloaded_file_names(kind_of_data_in_table)
        elif same_dates == False:
            user_start_date_data_interval = question_is_digit_and_date('Enter START date data interval ( e.g. 2011,7,21 ) : ')
            user_stop_date_data_interval = question_is_digit_and_date('Enter STOP date data interval ( e.g. 2011,7,22 ) : ')
            list_file_names_station_2 = down_data_in_parts(user_hisparc_station_id_2, user_start_date_data_interval, user_stop_date_data_interval)

            if list_file_names_station_2:
                pass
            else:
                sys.exit()
            kind_of_data_in_station_2 = kind_of_data(list_file_names_station_2)
            kind_of_data_in_table.extend(kind_of_data_in_station_2)
            show_downloaded_file_names(kind_of_data_in_table)

print ''

plot_question = query_yes_no('Do you want to see a PLOT of your data (variable against timestamp)?')

if plot_question == True and download_question == False:
    use_downloaded_files = False
    print ''
    print 'If you want to analyze data you must already have a data set on your pc.'
    print 'Make sure it is located at: ' + os.getcwd()

elif plot_question == True and download_question == True:
    use_downloaded_files = query_yes_no('Do you want to use the data you downloaded earlier?')


if plot_question == True and use_downloaded_files == True:
    plot_variable1 = choose_one_variable(kind_of_data_in_table, stations) #e.g. plot_variable = [('event_rate','data_s501_2011,12,7 - 2011,12,8.h5','501','events','')]
    values1, times, returntype = plot_data(plot_variable1)

if plot_question == True and use_downloaded_files == False:
    list_files = []
    stations = []

    print ''
    station_ID = question_is_digit("Enter the station ID that you want to use in your analysis ( e.g. '501' ) ")

    stations.append(station_ID)
    print ''
    number_of_files = question_is_digit("Enter the NUMBER of FILENAMES for station " + station_ID + " that you want to use in your analysis( e.g. '6' ): ")
    print ''
    print "You are going to enter filenames ( e.g. 'data_s501_2011,7,21 - 2011,7,22.h5' )"
    print 'Enter the filenames in CHRONOLOGICAL ORDER. '
    print ''
    for j in range(1, int(number_of_files)+1):
        while True:
            filename = raw_input('For station ' + station_ID + ' enter filename number ' + str(j) + ': ')
            ID = get_station_ID_from_filename(filename)
            if ID in stations:
                list_files.append(filename) # pas 'kind of data' aan zodat kijkt of hetzelfde station
                break
            else:
                print "Oops! The filename you entered does not match the station ID you entered earlier. Try again..."

    kind_of_data_in_table = kind_of_data(list_files) # e.g.  [('data_s501_2011,6,30 - 2011,6,30.h5', True, True), ('data_s502_2011,6,30 - 2011,6,30.h5', True, False)]
    plot_variable1 = choose_one_variable(kind_of_data_in_table, stations) #e.g. plot_variable = [('event_rate','data_s501_2011,12,7 - 2011,12,8.h5','501','events','')]
    values1, times, returntype = plot_data(plot_variable1)


print ''
correlate_question = query_yes_no('Do you want to CORRELATE data?')

use_plotted_files = False

if plot_question == True and correlate_question == True:
    use_plotted_files = query_yes_no('Do you want to use the data you plotted earlier?')
    if use_plotted_files == True:

        print ''
        print 'You are going to enter the specifications for the OTHER variable for correlation'
        print ''

        list_files = []
        stations = []

        print ''
        station_ID = question_is_digit("Enter the station ID that you want to use in your analysis ( e.g. '501' ) ")

        stations.append(station_ID)
        print ''
        number_of_files = question_is_digit("Enter the NUMBER of FILENAMES for station " + station_ID + " that you want to use in your analysis( e.g. '6' ): ")
        print ''
        print "You are going to enter filenames ( e.g. 'data_s501_2011,7,21 - 2011,7,21.h5' )"
        print 'Enter the filenames in CHRONOLOGICAL ORDER. '
        print ''
        for j in range(1, int(number_of_files)+1):
            while True:
                filename = raw_input('For station ' + station_ID + ' enter filename number ' + str(j) + ': ')
                ID = get_station_ID_from_filename(filename)
                print stations
                if ID in stations:
                    list_files.append(filename)
                    break
                else:
                    print "Oops! The filename you entered does not match the station ID you entered earlier. Try again..."
        kind_of_data_in_table = kind_of_data(list_files) # e.g.  [('data_s501_2011,6,30 - 2011,6,30.h5', True, True), ('data_s502_2011,6,30 - 2011,6,30.h5', True, False)]
        plot_variable2 = choose_one_variable(kind_of_data_in_table, stations) #e.g. plot_variable = [('event_rate','data_s501_2011,12,7 - 2011,12,8.h5','501','events')]

        if returntype == 'MPV':
            if len(times) > 1:
                mean_variable_list = get_corresponding_values_MPV(plot_variable2,times)
                filen = create_correlation_table(plot_variable1,plot_variable2, values1, mean_variable_list,int(times[1] - times[0]))
                least_squares_fit(filen, plot_variable1, plot_variable2)
            else:
                print 'Correlation is not possible with one data point.'

        elif returntype == 'whole':
            print 'b'
            filen = interpolate(plot_variable1,plot_variable2) # e.g. cor_data_barometer_501_event_rate_502.h5
            least_squares_fit(filen, plot_variable1, plot_variable2)

        elif returntype == 'part':
            complementary_variable2_list = get_corresponding_values_selection(plot_variable2,times)
            filen = interpolate_selection(array(zip(times,values1)),complementary_variable2_list)
            least_squares_fit(filen, plot_variable1, plot_variable2)

        else:
            print 'problem'

print ''
if correlate_question == True and download_question == False and use_plotted_files == False:
    use_downloaded_files = False
    print ''
    print 'If you want to analyze data you must already have a data set on your pc.'
    print 'Make sure it is located at: ' + os.getcwd()

elif correlate_question == True and download_question == True and use_plotted_files == False:
    use_downloaded_files = query_yes_no('Do you want to use the data you downloaded earlier?')


if correlate_question == True and use_downloaded_files == True and use_plotted_files == False:
    #e.g. variable1 = [('event_rate','data_s501_2011,12,7 - 2011,12,8.h5','501','events')]
    variable1, variable2 = choose_variables_for_correlation(kind_of_data_in_table, stations)
    filen = interpolate(variable1,variable2) # e.g. cor_data_barometer_501_event_rate_502.h5
    least_squares_fit(filen, variable1, variable2)

if correlate_question == True and use_downloaded_files == False and use_plotted_files == False:
    print ''
    number_of_stations = question_is_digit_with_constraint("Enter the NUMBER of STATION IDs that you want to use in your analysis( e.g. '2' ): ")
    list_files = []
    stations = []
    for i in range(1, int(number_of_stations)+1):
        print ''
        station_ID = question_is_digit("Enter the station ID for station " + str(i) + ': ')

        stations.append(station_ID)
        print ''
        number_of_files = question_is_digit("Enter the NUMBER of FILENAMES for station " + station_ID + " that you want to use in your analysis( e.g. '6' ): ")
        print ''
        print "You are going to enter filenames ( e.g. 'data_s501_2011,7,21 - 2011,7,21.h5' )"
        print 'Enter the filenames in CHRONOLOGICAL ORDER. '
        print ''
        for j in range(1, int(number_of_files)+1):
            while True:
                filename = raw_input('For station ' + str(i) + ' enter filename number ' + str(j) + ': ')
                ID = get_station_ID_from_filename(filename)
                if ID in stations:
                    list_files.append(filename) # pas 'kind of data' aan zodat kijkt of hetzelfde station
                    break
                else:
                    print "Oops! The filename you entered does not match the station ID you entered earlier. Try again..."

    kind_of_data_in_table = kind_of_data(list_files) # e.g.  [('data_s501_2011,6,30 - 2011,6,30.h5', True, True), ('data_s502_2011,6,30 - 2011,6,30.h5', True, False)]

    variable1, variable2 = choose_variables_for_correlation(kind_of_data_in_table, stations) # e.g. [('barometer', 'data_s501_2011,6,30 - 2011,6,30.h5', '501', 'weather')], [('event_rate', 'data_s502_2011,6,30 - 2011,6,30.h5', '502', 'events')]
    filen = interpolate(variable1,variable2) # e.g. cor_data_barometer_501_event_rate_502.h5
    least_squares_fit(filen, variable1, variable2)

