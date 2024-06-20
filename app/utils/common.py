from datetime import datetime


def now():
    now_string = datetime.now()
    return now_string.strftime("%Y-%m-%d %H:%M:%S")


def filter_secondary_deleted(secondary, item):
    results = []
    for record in secondary:
        if record.deleted_at is None:
            results.append(getattr(record, item))
    return results
