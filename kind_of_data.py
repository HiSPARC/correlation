
import tables
from get_station_ID_from_filename import get_station_ID_from_filename

def kind_of_data(list_file_names):

    muon_data_present_in_table = []
    weather_data_present_in_table = []

    for i in list_file_names:
        user_hisparc_station_id = get_station_ID_from_filename(i)
        data = tables.openFile(i, 'r')
        group =  'data.root.s%s' % user_hisparc_station_id

        if 'events' in eval(group):
            muon_data_present_in_table.append(True)
        else:
            muon_data_present_in_table.append(False)

        if 'weather' in eval(group):
            weather_data_present_in_table.append(True)
        else:
            weather_data_present_in_table.append(False)

        data.close()

    kind_of_data_in_table = zip(list_file_names, muon_data_present_in_table, weather_data_present_in_table)

    return kind_of_data_in_table

"""

list1 = ['data_s502_2011,6,30 - 2011,6,30.h5','data_s502_2011,7,1 - 2011,7,31.h5','data_s502_2011,8,1 - 2011,8,3.h5']
ID1 = '502'
list2 = ['data_s501_2011,6,30 - 2011,6,30.h5','data_s501_2011,7,1 - 2011,7,31.h5','data_s501_2011,8,1 - 2011,8,3.h5']
ID2 = '501'

table1 = kind_of_data(list1, ID1)
table1.extend(kind_of_data(list2, ID2))
print table1

dat = open('hallo.py', 'w')
for i in table1:
    dat.write(str(i))

"""


