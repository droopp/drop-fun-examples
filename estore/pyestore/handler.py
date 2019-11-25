from estore import get_events_by_device


def get(session, uri, headers, args, data):

    if uri == "/api/pyestore_async/events":
        return get_events_by_device(session, args)


def post(session, uri, headers, args, data):
    return 2


def put(uri, headers, args, data):
    return 3


def patch(uri, headers, args, data):
    return 4


def delete(uri, headers, args, data):
    return 5
