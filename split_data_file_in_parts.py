import tables
from scipy import array
from datetime import date, datetime

def get_number_of_variable_values(var_data):
    if len(var_data.shape) != 1:
        p1 = var_data[:,0]
        p2 = var_data[:,1]
        p3 = var_data[:,2]
        p4 = var_data[:,3]
        del var_data

        plate_list = []
        if sorted(p1)[-1] != -1:
            plate_list.append(True)
        if sorted(p2)[-1] != -1:
            plate_list.append(True)
        if sorted(p3)[-1] != -1:
            plate_list.append(True)
        if sorted(p4)[-1] != -1:
            plate_list.append(True)
        number_of_plates = len(plate_list)

    elif len(var_data.shape) == 1:
        number_of_plates = 1

    return number_of_plates

def split_data_file_in_parts(variable, seconds):

    dat_sorted = []

    for i in range(len(variable)):

        station_ID = variable[i][2]
        data = tables.openFile(variable[i][1],'r')

        tree = 'data.root.s' + station_ID + "." + variable[i][3] + "[:]['timestamp']"
        ts = eval(tree)

        tree = 'data.root.s' + station_ID + "." + variable[i][3] + "[:]['" + variable[i][0] + "']"
        var_data = eval(tree)
        data.close()

        list = []
        if len(var_data.shape) != 1: # check if it is an array of values

            p1 = var_data[:, 0]
            p2 = var_data[:, 1]
            p3 = var_data[:, 2]
            p4 = var_data[:, 3]
            del var_data

            plate_list = []
            if sorted(p1)[-1] != -1:
                plate_list.append(True)
            if sorted(p2)[-1] != -1:
                plate_list.append(True)
            if sorted(p3)[-1] != -1:
                plate_list.append(True)
            if sorted(p4)[-1] != -1:
                plate_list.append(True)

            number_of_plates = len(plate_list)

            if number_of_plates == 4:
                list = zip(p1.tolist(), p2.tolist(), p3.tolist(), p4.tolist())
            elif number_of_plates == 2:
                list = zip(p1.tolist(), p2.tolist())

        elif len(var_data.shape) == 1: # check if it is an array of values
            list = var_data.tolist()
            del var_data
        else:
            'weird!'
            pass

        dat_sorted_part = sorted(zip(ts,list))
        dat_sorted.extend(dat_sorted_part)

    begin = dat_sorted[0][0] # set begin equal to first timestamp e.g. 1323302400

    # make list with the index of every first of every time interval of seconds (e.g. every hour if 'seconds' = 86400)

    time_interval_list = []

    for i in range(len(dat_sorted)):
        if dat_sorted[i][0] >= begin:
            time_interval_list.append(i)

            begin = dat_sorted[i][0] - (dat_sorted[i][0] - begin) + seconds # kijk hier nog even naar
    # e.g. begin = 1323302400 - (1323302400  - 1323302400) + 86400 = 1323302400 - 0 + 86400 = 1323388800
    # e.g. begin = 1323388804 - (1323388804  - 1323388800) + 86400 = 1323388804 - 4 + 86400 = 1323475200
    # e.g. begin = 1323475200 - (1323475200  - 1323475200) + 86400 = 1323475200 - 0 + 86400 = 1323561600
    # e.g. begin = 1323561601 - (1323561601  - 1323561600) + 86400 = 1323561601 - 1 + 86400 = 1323648000 etc.


    # make list with the timestamps in the middle of every time interval (for later use in plot)
    times_timestamp = [dat_sorted[0][0] + (seconds/2) + i*seconds for i in range(len(time_interval_list))]


    # e.g. time_interval_list = [1000000000, 1000001000, 100002000, 1000003000, 1000004000]
    # e.g seconds = 1000

    # e.g. times_timestamp = 1000000000 + 1000/2 + 0*1000 = 1000000000 + 500 + 0    = 1000000500
    # e.g. times_timestamp = 1000000000 + 500    + 1*1000 = 1000000000 + 500 + 1000 = 1000001500
    # e.g. times_timestamp = 1000000000 + 500    + 2*1000 = 1000000000 + 500 + 2000 = 1000002500 etc.

    # split data list (timestamp, variable) into n chunks each containing around n seconds of data
    time_chunks = []

    for j in range(len(time_interval_list)):
        if j != range(len(time_interval_list))[-1]:
            time_chunks.append(dat_sorted[time_interval_list[j]:time_interval_list[j + 1]])
        else:
            time_chunks.append(dat_sorted[time_interval_list[j]:len(dat_sorted)])

    del time_interval_list

    variable_list_in_n_parts = [] # e.g. list containing n days of part_plist

    for day in time_chunks:
        # e,g, list with pulseheights of n plates (timestamps removed)
        list_with_pulseheights = [i[1] for i in day]
        variable_list_in_n_parts.append(array(list_with_pulseheights))

    return variable_list_in_n_parts, times_timestamp, number_of_plates


if __name__=="__main__":
    variable = [('pulseheights', 'data_s501_2011,12,8_2011,12,12.h5', '501', 'events')]
    #variable = [('integrals','data_s501_2011,12,7_2011,12,8.h5','501','events','')]
    #variable = [('pulseheights','data_s501_2011,12,7_2011,12,8.h5','501','events'),('pulseheights','data_s501_2011,12,8_2011,12,9.h5','501','events')]

    #variable = [('barometer','data_s501_2011,12,7_2011,12,8.h5','501','weather','')]
    seconds = 86400

    list, times = split_data_file_in_parts(variable,seconds)

