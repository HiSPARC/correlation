import tables


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
            shower_var = eval('data.root.s%s.events.colnames' % stationID)

        if file[2] == True:
            weather_var = eval('data.root.s%s.weather.colnames' % stationID)

        if file[1] == True | file[2] == True:
            if variable in weather_var:
                kind = 'weather'
            elif variable in shower_var:
                kind = 'events'

        return kind
    else:
        print 'problem'
