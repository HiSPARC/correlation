import tables

import question


def select_variable(kind_of_data_in_table, station):
    stationID = str(station)
    filename = kind_of_data_in_table[0][0]
    variables = [] # needed for module 'question.variable'
    variable = []

    for j in kind_of_data_in_table:
        if variable:
            break
        if not variable:
            filename = j[0]
            if stationID in filename:
                data = tables.openFile(filename, 'r')
                if j[1] == True:
                    shower_var = eval('data.root.s%s.events.colnames' % stationID)
                    # Remove for novice students useless shower variables
                    if 'event_id' in shower_var:
                        index = shower_var.index('event_id')
                        del shower_var[index]
                    if 'data_reduction' in shower_var:
                        index = shower_var.index('data_reduction')
                        del shower_var[index]
                    if 'trigger_pattern' in shower_var:
                        index = shower_var.index('trigger_pattern')
                        del shower_var[index]
                    if 'traces' in shower_var:
                        index = shower_var.index('traces')
                        del shower_var[index]

                    variables.extend(shower_var)
                    print ''
                    print 'SHOWER variables:'
                    print ''
                    for k in shower_var:
                        print '-' + k

                if j[2] == True:
                    weather_var = eval('data.root.s%s.weather.colnames' % stationID)

                    if 'event_id' in weather_var:
                        index = weather_var.index('event_id')
                        del weather_var[index]

                    variables.extend(weather_var)
                    print ''
                    print 'WEATHER variables:'
                    print ''

                    for l in weather_var:
                        print '-' + l
                data.close()

                if j[1] == True | j[2] == True:
                    print ''
                    print 'The variables from station %s are shown above.' % stationID
                    var = question.variable("Enter the variable from station %s that you want to use in your analysis ( e.g. 'event_rate' ) : " % stationID, variables)
                    variable.append(var)
                    returnvar = variable[0]
        else:
            break
    return returnvar
