from select_variable import select_variable
from kind_of_variable import kind_of_variable

def choose_variables_for_correlation(kind_of_data_in_table, stations):

    variable1 = []
    variable2 = []

    variable1_specs = []
    variable2_specs = []

    variables1 = []
    stationIDs1 = []
    filenames1 = []
    kinds1 = []


    variables2 = []
    stationIDs2 = []
    filenames2 = []
    kinds2 = []


    kind = ''

    if len(stations) == 1:
        if not variable1:
            #'select var1 from station 1'
            variable1 = select_variable(kind_of_data_in_table,stations[0])
            #'create variable specifications for var1 from station 1'
            for i in kind_of_data_in_table:
                kind = kind_of_variable(i,stations[0], variable1)
                variables1.append(variable1)
                stationIDs1.append(stations[0])
                filenames1.append(i[0])
                kinds1.append(kind)

            variable1_specs = zip(variables1,filenames1, stationIDs1,kinds1)

        if variable1:
            #'select var2 from station 1'
            variable2 = select_variable(kind_of_data_in_table,stations[0])
            #'create variable specifications for var2 from station 1'
            for i in kind_of_data_in_table:
                kind = kind_of_variable(i,stations[0], variable2)
                variables2.append(variable2)
                stationIDs2.append(stations[0])
                filenames2.append(i[0])
                kinds2.append(kind)

            variable2_specs = zip(variables2,filenames2, stationIDs2,kinds2)

    if len(stations) == 2:
        if not variable1:
            #'select var1 from station 1'
            variable1 = select_variable(kind_of_data_in_table,stations[0])
            #'create variable specifications for var1 from station 1'
            for i in kind_of_data_in_table:
                if str(stations[0]) in i[0]:
                    kind = kind_of_variable(i,stations[0], variable1)
                    variables1.append(variable1)
                    stationIDs1.append(stations[0])
                    filenames1.append(i[0])
                    kinds1.append(kind)

                    variable1_specs = zip(variables1,filenames1, stationIDs1,kinds1)
        if variable1:
            #'select var2 from station 2'
            variable2 = select_variable(kind_of_data_in_table,stations[1])
            for i in kind_of_data_in_table:
                if str(stations[1]) in i[0]:
                    kind = kind_of_variable(i,stations[1], variable2)
                    variables2.append(variable2)
                    stationIDs2.append(stations[1])
                    filenames2.append(i[0])
                    kinds2.append(kind)

                    variable2_specs = zip(variables2,filenames2, stationIDs2,kinds2)

    return variable1_specs, variable2_specs

    #stations = [502,501]
    #kind_of_data_in_table = [('data_s502_2011,6,30 - 2011,6,30.h5', True, False),('data_s502_2011,7,1 - 2011,7,31.h5', True, False),('data_s502_2011,8,1 - 2011,8,3.h5', True, False),('data_s501_2011,6,30 - 2011,6,30.h5', True, True),('data_s501_2011,7,1 - 2011,7,31.h5', True, True),('data_s501_2011,8,1 - 2011,8,3.h5', True, True)]

    #stations = [501]
    #kind_of_data_in_table = [('data_s501_2011,6,30 - 2011,6,30.h5', True, True),('data_s501_2011,7,1 - 2011,7,31.h5', True, True),('data_s501_2011,8,1 - 2011,8,3.h5', True, True)]
