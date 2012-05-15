from select_variable import select_variable 
from kind_of_variable import kind_of_variable
from question_is_digit_station import question_is_digit_station


def choose_one_variable(kind_of_data_in_table, stations):
    
    if len(stations) > 1:
        for station in stations:
            print '-You have data for station %s' % (str(station)) 
        
        print ''
        station_ID = question_is_digit_station('Enter the station ID that you want to use. ',stations)
    else:
        station_ID = stations[0]
    
    variables1 = []
    stationIDs1 = []
    filenames1 = []
    kinds1 = []

    variable1_specs = []
            
    #'select variable from station'
    variable1 = select_variable(kind_of_data_in_table,station_ID)
    #'create variable specifications for variable'
    for i in kind_of_data_in_table:
        if station_ID in i[0]:
            kind = kind_of_variable(i,station_ID, variable1)
            variables1.append(variable1)
            stationIDs1.append(station_ID)
            filenames1.append(i[0])
            kinds1.append(kind)

            
        else:
            pass
    
    variable1_specs = zip(variables1,filenames1, stationIDs1,kinds1)
    #e.g. variable1_specs = [('event_rate','data_s501_2011,12,7 - 2011,12,8.h5','501','events','')] 
    
    return variable1_specs

"""    
stations = [501,8001]
kind_of_data_in_table = [('data_s501_2011,12,7 - 2011,12,8.h5', True, True),('data_s8001_2011,12,7 - 2011,12,8.h5', True, False)]


var_specs = choose_variables_to_plot(kind_of_data_in_table, stations)
print var_specs
"""

