
def show_downloaded_file_names(kind_of_data_in_table):
    print ' _____________________________________________________________'
    print '|                                                             |'
    print '| You have downloaded the file(s):       containing data of:  |'
    print '|                                                             |'
    print '|                                        SHOWER WEATHER       |'
    print '|                                                             |'
    blank = '|                                                             |'
    for i in kind_of_data_in_table:
        length_string = len(i[0]) + len(str(i[1])) + len(str(i[2]))
        if length_string <= 51:
            print '| ' + str(i) + blank[2+length_string:]
        else:
            print i[0], length_string
    print '|_____________________________________________________________|'
