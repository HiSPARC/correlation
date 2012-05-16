def get_station_ID_from_filename(filename):
    a = filename.partition('_s')
    b = str(a[2]).partition('_')
    return b[0]