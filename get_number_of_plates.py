def get_number_of_plates(variable):
    
    plate_list = []
    for val in variable:
        if val == -1:
            pass
        else:
            plate_list.append(val)
    
    number_of_plates = len(plate_list)
    return number_of_plates