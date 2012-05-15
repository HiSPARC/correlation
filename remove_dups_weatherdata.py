import tables
import operator

def remove_dups_weatherdata(data, group):
    """Remove duplicate rows from event table

    :param data: PyTables file handle
    :param group: PyTables group containing the weather data table

    """
    events = group.weather

    ts = [x for x in enumerate(events[:]['timestamp'])]
    ts.sort(key=operator.itemgetter(1))

    prev = 0
    clist = []
    for i, t in ts:
        if t != prev:
            clist.append(i)
        prev = t

    clist.sort()
    print "Removing %d duplicate rows of weather data" % (len(events) - len(clist))

    if len(clist) != len(events):
        tmptable = data.createTable(group, 't__events',
                                    description=events.description)
        rows = events.readCoordinates(clist)
        tmptable.append(rows)
        tmptable.flush()

        data.renameNode(tmptable, events._v_name, overwrite=True)
