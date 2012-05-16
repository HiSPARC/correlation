
def show_downloaded_file_names(kind_of_data_in_table):
    print ' _____________________________________________________________'
    print '|                                                             |'
    print '| You have downloaded the file(s):       containing data of:  |'
    print '|                                                             |'
    print '|                                        SHOWER WEATHER       |'
    print '|                                                             |'
    for i in kind_of_data_in_table:
        length_string = len(i[0])+ len(str(i[1])) + len(str(i[2]))
        if length_string == 37:
            print '| '+ str(i) + '               |'
        elif length_string == 38:
            print '| '+ str(i) + '              |'
        elif length_string == 39:
            print '| '+ str(i) + '             |'
        elif length_string == 40:
            print '| '+ str(i) + '            |'
        elif length_string == 41:
            print '| '+ str(i) + '           |'
        elif length_string == 42:
            print '| '+ str(i) + '          |'
        elif length_string == 43:
            print '| '+ str(i) + '         |'
        elif length_string == 44:
            print '| '+ str(i) + '        |'
        elif length_string == 45:
            print '| '+ str(i) + '       |'
        elif length_string == 46:
            print '| '+ str(i) + '      |'
        elif length_string == 47:
            print '| '+ str(i) + '     |'
        elif length_string == 48:
            print '| '+ str(i) + '    |'
        elif length_string == 49:
            print '| '+ str(i) + '   |'
        else:
            print i[0], length_string

    print '|_____________________________________________________________|'