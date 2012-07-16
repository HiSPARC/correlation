import re
import os
import time
from datetime import datetime as dt, timedelta
import urllib2
import httplib

from query_yes_no import query_yes_no


def search_operational_stations():
    """Find active HiSPARC shower and weather stations"""

    if os.path.isfile('active_station_IDs.txt'):
        read_list_from_file()
    else:
        print ''
        print 'You do not have a list with operational stations in your current working directory.'

    update = query_yes_no('Do you want to update/create the list with operational stations?')
    print ''

    if update == True:
        active_shower, active_weather = get_active_stations()
        with open('active_station_IDs.txt', 'w') as file:
            file.write('active_shower = [')
            file.write(', '.join(str(id) for id in active_shower))
            file.write(']\nactive_weather = [')
            file.write(', '.join(str(id) for id in active_weather))
            file.write(']')
        read_list_from_file()


def read_list_from_file():
    """Read the file with the list of active stations"""

    print ''
    print ('The last check for operational stations was at: ' +
           time.ctime(os.path.getctime('active_station_IDs.txt')))
    print ''

    execfile('active_station_IDs.txt', globals())

    print '- At that time the following HiSPARC stations were operational:'
    print active_shower
    print ''
    print '- And the following WEATHER stations were operational:'
    print active_weather
    print ''


def get_active_stations():
    """Check which of the given stations had any shower or weather data yesterday"""

    station_ids = get_station_ids()
    active_stations = active_station(station_ids)
    active_shower = active_shower_station(active_stations)
    active_weather = active_weather_station(active_stations)

    return active_shower, active_weather


def active_shower_station(station_ids):
    """Check which of the given stations had any shower data yesterday"""

    active_ids = []
    for id in station_ids:
        url = "/django/show/source/eventtime/%s/%s" % (id, yesterday_url())
        if url_exists(url):
            active_ids.append(id)
    return active_ids


def active_weather_station(station_ids):
    """Check which of the given stations had any weather data yesterday"""

    active_ids = []
    for id in station_ids:
        url = "/django/show/source/barometer/%s/%s" % (id, yesterday_url())
        if url_exists(url):
            active_ids.append(id)
    return active_ids


def active_station(station_ids):
    """Check which of the given stations had any data yesterday"""

    active_ids = []
    for id in station_ids:
        url = "/django/show/stations/%s/%s" % (id, yesterday_url())
        if url_exists(url):
            active_ids.append(id)
    return active_ids


def get_station_ids():
    """Get list of all station ids from the Station List page"""

    url = "http://data.hisparc.nl/django/show/stations/"
    page = urllib2.urlopen(url).read()
    regex = '(?<=/show/stations/)[0-9]+'
    id_strings = re.findall(regex, page)
    station_ids = [int(id) for id in id_strings]
    station_ids.sort()
    return station_ids


def url_exists(url, base="data.hisparc.nl"):
    """Check if the url exists (returns 200)"""

    conn = httplib.HTTPConnection(base)
    conn.request("HEAD", url)
    res = conn.getresponse()
    return res.status in (200, )


def yesterday_url():
    """Make the part of the url for the date (yesterday)"""

    yesterday = dt.now() - timedelta(days = 1)
    url = "%s/%s/%s/" % (yesterday.year, yesterday.month, yesterday.day)
    return url


if __name__ == '__main__':
    search_operational_stations()
