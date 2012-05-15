""" Process HiSPARC / KASCADE coincidences

    This module reads data from the HiSPARC and KASCADE event tables and
    searches for coincidences.

"""
import datetime
import time
import os
import operator

try:
    import pylab
except ImportError:
    pass

def do_timeshifts(hevents, kevents, shifts, dtlimit=None, limit=None,
                  h=None, k=None):
    """Search for coincidences using multiple time shifts

    This function enables you to search for coincidences multiple times,
    using a list of time shifts. Given a data file, the events are read
    into arrays and passed on to the search_coincidences function. For
    each shift, a histogram is plotted so you can get a feel for the
    goodness of the shift. The coincidences data from the last shift is
    returned.

    :param hevents: hisparc event table
    :param kevents: kascade event table
    :param shifts: a list of time shifts
    :param dtlimit: limit on the time difference between hisparc and
        kascade events in nanoseconds.  If this limit is exceeded,
        coincidences are not stored.  Default: None.
    :param limit: an optional limit on the number of kascade events used
        in the search
    :param h: prefetched array from hisparc table (optional)
    :param k: prefetched array from kascade table (optional)

    :return: An array of coincidences from the last shift ([dt in
        nanoseconds, hisparc event id, kascade event id]).

    """
    # Get arrays from the tables. This is much, much faster than working
    # from the tables directly. Pity.
    if not h or not k:
        h, k = get_arrays_from_tables(hevents, kevents, limit)

    for shift in shifts:
        print "Calculating dt's for timeshift %.9f (%d nanoseconds)" % \
              (shift, long(shift * 1e9))
        coincidences = search_coincidences(h, k, shift, dtlimit)

        dt = [x[0] / 1e9 for x in coincidences]
        try:
            pylab.hist(dt, bins=100, range=(-1, 1), histtype='step',
                       label="Shift %+g s" % shift)
        except NameError:
            pass

    finish_graph()
    return coincidences

def store_coincidences(table, hevents, kevents, coincidences):
    """Store coincidences in a table

    This function stores coincidences which are found by
    search_coincidences in a table, so data can be easily retrieved without
    resorting to lookups which span multiple tables.

    :param table: table to hold the coincidences
    :param hevents: hisparc event table
    :param kevents: kascade event table
    :param coincidences: a list of coincidences, as given by
        search_coincidences

    """
    old_data_length = len(table)
    tablerow = table.row

    for coincidence in coincidences:
        hisparc = hevents[coincidence[1]]
        kascade = kevents[coincidence[2]]
        tablerow['event_id'] = hisparc['event_id']
        tablerow['k_event_id'] = kascade['event_id']
        tablerow['timestamp'] = hisparc['timestamp']
        tablerow['nanoseconds'] = hisparc['nanoseconds']
        tablerow['ext_timestamp'] = hisparc['ext_timestamp']
        tablerow['pulseheights'] = hisparc['pulseheights']
        tablerow['integrals'] = hisparc['integrals']
        tablerow['n_peaks'] = hisparc['n_peaks']
        tablerow['traces'] = hisparc['traces']
        tablerow['k_timestamp'] = kascade['timestamp']
        tablerow['k_nanoseconds'] = kascade['nanoseconds']
        tablerow['k_ext_timestamp'] = kascade['ext_timestamp']
        tablerow['k_energy'] = kascade['energy']
        tablerow['k_core_pos'] = kascade['core_pos']
        tablerow['k_zenith'] = kascade['zenith']
        tablerow['k_azimuth'] = kascade['azimuth']
        tablerow['k_Num_e'] = kascade['Num_e']
        tablerow['k_Num_mu'] = kascade['Num_mu']
        tablerow['k_dens_e'] = kascade['dens_e']
        tablerow['k_dens_mu'] = kascade['dens_mu']
        tablerow['k_P200'] = kascade['P200']
        tablerow['k_T200'] = kascade['T200']
        tablerow.append()
    table.flush()

    # Flush old data
    if old_data_length:
        print "Flushing old data..."
        table.removeRows(0, old_data_length)

def search_coincidences(hisparc_data, kascade_data, timeshift,
                        dtlimit=None):
    """Search for coincidences

    This function does the actual searching of coincidences. It uses a
    timeshift to shift the HiSPARC data (we know that these employ GPS
    time, so not taking UTC leap seconds into account). The shift will also
    compensate for delays in the experimental setup.

    :param hisparc_data: an array containing the hisparc data
    :param kascade_data: an array containing the kascade data
    :param timeshift: the amount of time the HiSPARC data are shifted (in
        seconds)
    :param dtlimit: limit on the time difference between hisparc and
        kascade events in nanoseconds.  If this limit is exceeded,
        coincidences are not stored.  Default: None.

    :return: An array of time differences and event ids of each KASCADE
        event and the nearest neighbour HiSPARC event.

    """
    # Shift the kascade data instead of the hisparc data. There is less of
    # it, so this is much faster.
    k = shift_data(kascade_data, -timeshift)
    h = hisparc_data

    coincidences = []

    # First loop through kascade data until we have the first event that
    # occurs _after_ the first hisparc event.
    h_idx = 0
    for k_idx in range(len(k)):
        if k[k_idx][1] > h[h_idx][1]:
            break

    while True:
        # Try to get the timestamps of the kascade event and the
        # neighbouring hisparc events.
        try:
            h_t = h[h_idx][1]
            k_t = k[k_idx][1]
            h_t_next = h[h_idx + 1][1]
        except IndexError:
            # Reached beyond the event list.
            break

        # Make sure that while the current hisparc event is _before_ the
        # kascade event, the next hisparc event should occur _after_ the
        # kascade event.  That way, the kascade event is enclosed by
        # hisparc events.
        if k_t > h_t_next:
            h_idx += 1
            continue

        # Calculate the time differences for both neighbors. Make sure to
        # get the sign right. Negative sign: the hisparc event is 'left'.
        # Positive sign: the hisparc event is 'right'.
        dt_left = h_t - k_t
        dt_right = h_t_next - k_t

        # Determine the nearest neighbor and add that to the coincidence
        # list, if dtlimit is not exceeded
        if dtlimit is None or min(abs(dt_left), abs(dt_right)) < dtlimit:
            if abs(dt_left) < abs(dt_right):
                coincidences.append((dt_left, h_idx, k_idx))
            else:
                coincidences.append((dt_right, h_idx + 1, k_idx))

        # Found a match for this kascade event, so continue with the next
        # one.
        k_idx += 1

    return coincidences

def shift_data(data, timeshift):
    """Shift event data in time

    This function shifts the event data in time, by specifying a timeshift
    in seconds. The original data is left untouched. Returns a new array
    containing the shifted data.

    :param data: the HiSPARC or KASCADE data to be shifted
    :param timeshift: the timeshift in seconds

    :return: an array containing the original data shifted in time

    """
    # convert timeshift to an integer value in nanoseconds
    timeshift = long(timeshift * 1e9)

    return [[x[0], x[1] + timeshift] for x in data]

def finish_graph():
    """Finish the histogram

    This function places a legend, axes titles and the like on the current
    figure.

    """
    try:
        pylab.legend()
        pylab.xlabel("Time difference (s)")
        pylab.ylabel("Counts")
        pylab.title("Nearest neighbour events for HiSPARC / KASCADE")
        pylab.gca().axis('auto')
        pylab.gcf().show()
    except NameError:
        print "Unfortunately, the pylab interface was not available."
        print "No graphs at this point."

def get_arrays_from_tables(h, k, limit=None):
    """Get data arrays from data tables

    This function returns an array of values extracted from the event
    tables with hisparc and kascade data. It honors a limit and only
    fetches events which fall inside the time window.

    Caveat: because the timeshift is not yet known, a few coincidences
    may fall outside the time window and not be taken into account.

    :param h: hisparc event table
    :param k: kascade event table
    :param limit: limit on the number of kascade events

    :return: Two arrays containing hisparc and kascade data ([event id,
        timestamp in nanoseconds])

    """
    try:
        k_t = k[limit - 1]['timestamp']
    except (IndexError, TypeError):
        k_t = k[-1]['timestamp']
    h_t = h[-1]['timestamp']

    t_end = min([k_t, h_t])

    k = [[x['event_id'], x['ext_timestamp']] for x in \
         k.where('timestamp <= t_end')]
    h = [[x['event_id'], x['ext_timestamp']] for x in \
         h.where('timestamp <= t_end')]

    # hisparc events are not necessarily sorted on timestamp
    h = sorted(h, key=operator.itemgetter(1))

    return h, k

def test(hevents, kevents, h=None, k=None):
    """Perform a small coincidence test

    Careful: the following search is limited to 1000 kascade events
    The complete statement would be:
    c = :func:`do_timeshifts(hevents, kevents, [-13.180220188408871])`

    :param hevents: hisparc event table
    :param kevents: kascade event table

    """
    print "Careful: the following search is limited to 1000 kascade events"
    print "The complete statement would be:"
    print "c = do_timeshifts(hevents, kevents, [-13.180220188408871])"
    return do_timeshifts(hevents, kevents, [-13.180220188408871],
                         limit=1000, h=h, k=k)
