import tables

from get_station_ID_from_filename import get_station_ID_from_filename


def check_if_weather(data, filename):

    user_hisparc_station_id = get_station_ID_from_filename(filename)
    table =  'data.root.'
    folder = 's' + user_hisparc_station_id
    group = table + folder

    if 'weather' in eval(group):
        weather_data_present_in_table = True
    else:
        weather_data_present_in_table = False

    return weather_data_present_in_table
