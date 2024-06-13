from datetime import datetime


def now():
    now_string = datetime.now()
    return now_string.strftime("%Y-%m-%d %H:%M:%S")
