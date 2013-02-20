import tables
import operator

def remove_duplicate_events(data, group, kind='events'):
    """Remove duplicate rows from hisparc or weather data

    :param data: PyTables file handle
    :param group: PyTables group containing the data node
    :param kind: PyTables node containing the events

    """
    if kind == 'weather':
        events = group.weather
        timestamps = [x for x in enumerate(events.col('timestamp'))]
    else:
        events = group.events
        timestamps = [x for x in enumerate(events.col('ext_timestamp'))]

    timestamps.sort(key=operator.itemgetter(1))

    prev = 0
    unique_list = []
    for unique_id, timestamp in timestamps:
        if timestamp != prev:
            unique_list.append(unique_id)
        prev = timestamp

    unique_list.sort()

    print ("Removing %d duplicate rows of shower data" %
           (len(events) - len(unique_list)))

    if len(unique_list) != len(events):
        tmptable = data.createTable(group, 't__events',
                                    description=events.description)
        rows = events.readCoordinates(unique_list)
        tmptable.append(rows)
        tmptable.flush()

        data.renameNode(tmptable, events._v_name, overwrite=True)
