import tables
from question_is_digit_with_plate_constraint import question_is_digit_with_plate_constraint

def kind_of_variable(file, station, variable):

    stationID = str(station)
    filename = file[0]
    shower_var = []
    weather_var = []
    kind = ''
    plate = ''

    if stationID in filename:
        data = tables.openFile(filename, 'r')
        if file[1] == True:
            shower_var = eval('data.root.s' + stationID + '.events.colnames')

        if file[2] == True:
            weather_var = eval('data.root.s' + stationID + '.weather.colnames')
        else:
            pass

        if file[1] == True | file[2] == True:
            if variable in weather_var:
                kind = 'weather'
            elif variable in shower_var:
                kind = 'events'

            else:
                pass
        return kind
    else:
        'problem'
        pass

"""
stations = [502,501]
kind_of_data_in_table = [('data_s502_2011,6,30 - 2011,6,30.h5', True, False),('data_s502_2011,7,1 - 2011,7,31.h5', True, False),('data_s502_2011,8,1 - 2011,8,3.h5', True, False),('data_s501_2011,6,30 - 2011,6,30.h5', True, True),('data_s501_2011,7,1 - 2011,7,31.h5', True, True),('data_s501_2011,8,1 - 2011,8,3.h5', True, True)]


#kind_of_data_in_table = [('data_s501_2011,6,30 - 2011,6,30.h5', True, True),('data_s501_2011,7,1 - 2011,7,31.h5', True, True),('data_s501_2011,8,1 - 2011,8,3.h5', True, True)]
file = kind_of_data_in_table[0]
#stations = [501]
variable = 'event_rate'


kind = kind_of_variable(file, stations[0], variable)


print kind
print 'hai'
"""
#table = select_variable(kind_of_data_in_table,stations)


