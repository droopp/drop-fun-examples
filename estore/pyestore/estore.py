##
# Estore func
#

from async import log

from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement
from cassandra import ReadTimeout

import time

import json

# import uuid
# import os
# import sys
from datetime import datetime, timedelta
# from datetime import timedelta
# from collections import OrderedDict

import gevent
from gevent.pool import Pool


FETCH_SIZE = 1000
GPOOL2 = 500
MAX_UNFINISHED = 72

_KINDS = {
    0: [0],

    # Common EStore event kinds. Used e.g. in VCFront.
    1: [1000],

    # Violet alarm event kinds.
    2: [20000, 20001, 20002, 20003, 20004, 20005, 20006, 20007, 20008, 20009,
        20100, 20101, 20102, 20103],

    # Remapped Violet notification event kinds.
    8: [80000, 80104, 80105, 80106, 80200, 80201, 80202, 80203, 80204, 80205,
        80206, 80207, 80208, 80209, 80210, 80211, 80212, 80213, 80214, 80215,
        80218, 80219, 80220, 80221, 80222, 80223, 80224, 80225],

    # VCFront event kinds.
    4: [40000, 40001],

    #  CCAgent event kinds.
    6: [60000],

    # Serverside detectors event kinds.
    7: [70000],

    # CSUploader event kinds.
    9: [90000, 90001]

}


def timeit(method):
    def timed(*args):
        ts = time.time()
        result = method(*args)
        log("func {} elapsed {}".format(method.__name__, (time.time() - ts)))
        return result

    return timed


@timeit
def get_event_by_device0(args):

    session, _uuid, hour, msg = args

    _source, _kinds = get_source_kinds(msg.get("source"), msg.get("kinds"))

    # log("get_source_kinds {} {}".format(_source, _kinds))

    if _source is None or _kinds is None:
        return "bad request: source {}, kinds {}".format(_source, _kinds)

    _end_m = parse_date(msg.get("end_ge", "9999-01-01t00:00:00.00z"))
    _begin_m = parse_date(msg.get("begin_le", "1900-01-01t00:00:00.00z"))

    placeholders = ','.join([str(x) for x in _kinds])  # "%s, %s, %s, ... %s"

    # log("placeholders  {}".format(placeholders))

    _cql = """SELECT device_uuid,
                     uuid,
                     source,
                     kind,
                     begin_time,
                     end_time,
                     properties

            FROM events_by_device

            WHERE device_uuid = {}
                AND hour = '{}'
                AND kind IN ({})

            """.format(_uuid, hour, placeholders)

    # log(_cql)

    query = SimpleStatement(_cql, consistency_level=ConsistencyLevel.LOCAL_ONE, fetch_size=FETCH_SIZE)
    rows = session.execute(query)

    _events = []
    try:

        for row in rows:

            if row.begin_time > _end_m and row.end_time < _begin_m:

                _ev = {"id": hash(row[0]),
                       "device_uuid": str(row[0]),
                       "camera_uid": str(row[0]),
                       "uuid": str(row[1]),
                       "source": row[2],
                       "kind": row[3],
                       "begin_time": format_date(row[4]),
                       "end_time": format_date(row[5]),
                       "properties": json.loads(row[6])
                       }

                _events.append(_ev)
                # log("row: {}".format(row))

        # log("len of events {}".format(len(_events)))

        return _events

    except ReadTimeout:
        raise Exception("Read timeout")


@timeit
def get_long_events(args):

    session, _uuid, msg = args

    _source, _kinds = get_source_kinds(msg.get("source"), msg.get("kinds"))

    # log("get_source_kinds {} {}".format(_source, _kinds))

    if _source is None or _kinds is None:
        return "bad request: source {}, kinds {}".format(_source, _kinds)

    _end_m = parse_date(msg.get("end_ge", "9999-01-01t00:00:00.00z"))
    # _begin_m = parse_date(msg.get("begin_le", "1900-01-01t00:00:00.00z"))

    placeholders = ','.join([str(x) for x in _kinds])  # "%s, %s, %s, ... %s"

    # log("{} {}".format(_end_m, _begin_m))

    _cql = """SELECT device_uuid,
                     uuid,
                     source,
                     kind,
                     begin_time,
                     end_time,
                     properties

            FROM events_by_device_up10min

            WHERE device_uuid = {}
                AND kind IN ({})
                AND begin_time < '{}'
                AND begin_time > '{}'

            """.format(_uuid, placeholders, format_hour(_end_m + timedelta(hours=1)), format_hour(_end_m - timedelta(hours=MAX_UNFINISHED)))

    # log(_cql)

    query = SimpleStatement(_cql, consistency_level=ConsistencyLevel.LOCAL_ONE, fetch_size=FETCH_SIZE)
    rows = session.execute(query)

    _events = []
    try:

        for row in rows:

            # log("begin_time {} _end_m {} end_time {} _begin_m {}".format(row.begin_time, _end_m, row.end_time, _begin_m))
            if row.begin_time > _end_m:
                continue
            if row.end_time < _end_m:
                continue

            _ev = {"id": hash(row[0]),
                   "device_uuid": str(row[0]),
                   "camera_uid": str(row[0]),
                   "uuid": str(row[1]),
                   "source": row[2],
                   "kind": row[3],
                   "begin_time": format_date(row[4]),
                   "end_time": format_date(row[5]),
                   "properties": json.loads(row[6])
                   }

            _events.append(_ev)

            # log("row: {}".format(row))

        # log("len of long{}".format(len(_events)))

        return sorted(_events, key=lambda i: parse2_date(i['begin_time']), reverse=True)

    except ReadTimeout:
        raise Exception("Read timeout")


@timeit
def get_count_events_by_device(args):

    session, _uuid, msg = args

    _source, _kinds = get_source_kinds(msg.get("source"), msg.get("kinds"))

    # log("get_source_kinds {} {}".format(_source, _kinds))

    if _source is None or _kinds is None:
        return "bad request: source {}, kinds {}".format(_source, _kinds)

    _end_m = parse_date(msg.get("end_ge", "9999-01-01t00:00:00.00z"))
    _begin_m = parse_date(msg.get("begin_le", "1900-01-01t00:00:00.00z"))

    placeholders = ','.join([str(x) for x in _kinds])  # "%s, %s, %s, ... %s"

    # log("placeholders  {}".format(placeholders))

    _cql = """SELECT device_uuid, hour, kind, count

            FROM count_events_by_hour

            WHERE device_uuid = {}
                AND kind IN ({})
                AND hour >= '{}'
                AND hour <= '{}'

            """.format(_uuid, placeholders, format_hour(_end_m), format_hour(_begin_m))

    # log(_cql)

    query = SimpleStatement(_cql, consistency_level=ConsistencyLevel.LOCAL_ONE, fetch_size=FETCH_SIZE)
    rows = session.execute(query)

    try:

        n = 0
        _rows = {}

        for row in rows:
            n = n + row.count
            _key = str(row.device_uuid) + "=" + str(row.hour)

            _tmp = _rows.get(_key, 0)
            _rows[_key] = _tmp + row.count

        return {"data": _rows, "count": n}

    except ReadTimeout:
        raise Exception("Read timeout")


def get_events_by_device(session, msg):

    _uuids = msg["camera_uids"].split(",")

    _uuid = _uuids[0]

    pool = Pool(GPOOL2)

    # log("_uuid {}".format(_uuid))

    _source, _kinds = get_source_kinds(msg.get("source"), msg.get("kinds"))
    _end_m = parse_date(msg.get("end_ge", "9999-01-01t00:00:00z"))
    _begin_m = parse_date(msg.get("begin_le", "1900-01-01t00:00:00z"))

    log("dates {} {}".format(_end_m, _begin_m))

    if _source is None or _kinds is None:
        raise Exception("bad request: source {}, kinds {}".format(_source, _kinds))

    # placeholders = ','.join([str(x) for x in _kinds])  # "%s, %s, %s, ... %s"

    # log("placeholders  {}".format(placeholders))

    # pool = Pool2(GPOOL)

    jobs = []

    jobs.append(pool.spawn(get_count_events_by_device, (session, _uuid, msg)))
    jobs.append(pool.spawn(get_long_events, (session, _uuid, msg)))

    gevent.joinall(jobs)

    # log("JOBS {}".format(jobs))
    # counts = get_count_events_by_device((session, _uuid, msg))

    counts = jobs[0].value

    if counts is None:
        raise Exception("count query error")
    # log("count: {}".format(counts))

    # long_ev = get_long_events((session, _uuid, msg))

    long_ev = jobs[1].value
    if counts is None:
        raise Exception("long event query error")

    # log("long_ev: {}".format(long_ev))

    jobs = []
    for k in counts["data"].keys():
        log("get chunk {}".format(k))
        jobs.append(pool.spawn(get_event_by_device0, (session, _uuid, k.split("=")[1], msg)))

    gevent.joinall(jobs)

    events = []
    for j in jobs:
        if j.value is not None:
            events += j.value

    # log("events: {}".format(events))

    events = events + long_ev

    # log("final events: {}".format(events))

    # for i in events:
    #     log("{}".format(i["begin_time"]))

    # events = get_event_by_device0((session, _uuid, '2019-11-19 14:00:00', msg))

    # if _end_m is not None:
    #     long_events = get_long_events((session, _uuid, msg))
    return {"counts": len(events), "events": events}


def format_date(d):
    if d is not None:
        return datetime.strftime(d, '%Y-%m-%dT%H:%M:%S.%f')
    else:
        return None


def parse2_date(d):
    if d is not None:
        return datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%f')
    else:
        return None


def format_hour(d):
    if d is not None:
        return datetime.strftime(d, '%Y-%m-%dT%H:00:00')
    else:
        return None


def parse_date(d):
    return datetime.strptime(d, '%Y-%m-%dt%H:%M:%S.%fz')


def parse_json(d):
    try:
        return json.loads(d)
    except:
        return d


def extract_time(json):
    try:
        return time.mktime(parse_date(json['end_ge']).timetuple())
    except KeyError:
        return 0


def get_source_kinds(source, kind):

    # log("get_source_kinds {} {}".format(source, kind))

    if source is None and kind is not None:
        return int(str(kind)[0]), [kind]

    elif kind is None and source is not None:

        # log("get_source_kinds {} {}".format(source, _KINDS.get(source)))
        return source, _KINDS.get(source)

    else:
        return source, [kind]
