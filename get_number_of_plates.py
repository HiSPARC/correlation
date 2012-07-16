def get_number_of_plates(variable):

    plate_list = [val for val in variable if val != -1]
    number_of_plates = len(plate_list)

    return number_of_plates
