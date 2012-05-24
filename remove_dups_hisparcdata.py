import tables
import operator

def remove_dups(data, group):
    """Remove duplicate rows from event table

    :param data: PyTables file handle
    :param group: PyTables group containing the event table

    """
    events = group.events

    timestamps = [x for x in enumerate(events.col('ext_timestamp'))]
    timestamps.sort(key=operator.itemgetter(1))

    prev = 0
    unique_list = []
    for unique_id, timestamp in timestamps:
        if timestamp != prev:
            unique_list.append(unique_list)
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
