#!/usr/bin/env python3


import datetime, sys

if len(sys.argv) != 5:
    print('''Usage: ./calculate_stopped_cluster_time.py [target_power(PiB)] [sector_size(32|64)] [oneday_power(TiB)] [current_sector_number]
    eg:./calculate_stopped_cluster_time.py 4 32 200 4987''')
    exit(3)

target_power = float(sys.argv[1])
sector_size = int(sys.argv[2])
oneday_power = int(sys.argv[3])
current_sector_number = int(sys.argv[4])

spent_hour = (target_power * 1024 * 1024 / sector_size - current_sector_number) / (
        oneday_power * 1024 / sector_size) * 24 - 3

target_datetime = (datetime.datetime.now() + datetime.timedelta(hours=spent_hour)).strftime("%Y-%m-%d %H:%M:%S")

print(target_datetime)