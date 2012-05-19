
def show_downloaded_file_names(kind_of_data_in_table):
    print ' _____________________________________________________________'
    print '|                                                             |'
    print '| You have downloaded the file(s):       containing data of:  |'
    print '|                                                             |'
    print '|                                        SHOWER WEATHER       |'
    print '|                                                             |'
    for i in kind_of_data_in_table:
        print '| %-38s %-6s %-6s        |' % (i[0], str(i[1]), str(i[2]))
    print '|_____________________________________________________________|'
