#!/usr/bin/env python3

from datetime import datetime

def time_diff_from_now(timestamp):
    datetime_obj = datetime.fromisoformat(timestamp)
    current_datetime = datetime.now()
    time_diff = current_datetime - datetime_obj
    return time_diff.total_seconds()




if __name__ == '__main__':
    time = str(datetime.now())
    print("Time difference from now:", time_diff_from_now(time))
