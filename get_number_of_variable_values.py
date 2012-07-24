def get_number_of_variable_values(var_data):
    if len(var_data.shape) != 1:
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

    elif len(var_data.shape) == 1:
        number_of_plates = 1

    return number_of_plates


if __name__ == "__main__":
    import tables
    with tables.openFile('data_s502_2011,6,1 - 2011,7,1.h5', 'r') as data:
        colnames_events = data.root.s502.events.colnames

        for colname in colnames_events:
            var_string = "data.root.s502.events.col('%s')" % colname
            var = eval(var_string)

            number_of_plates = get_number_of_variable_values(var)
            print colname, number_of_plates


"""
var_data = data.root.s502.events[:]['pulseheights']

er = data.root.s502.events[:]['event_rate']
data.close()
var_data = var_data.tolist()
er.tolist()

p1,p2,p3,p4 = zip(*var_data)

print sorted(p3)[-1]
print sorted(p4)[-1]
"""
