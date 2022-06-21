import time, datetime
import argparse

parse = argparse.ArgumentParser()
# parse.add_argument('-h','--help', default='Usage: copy_calculate_days.py -t NUM -s DATETIME -c COPIED_NUMBER')
parse.add_argument('-t', '--total-number', type=int, required=True, help='-t option are required')
parse.add_argument('-s', '--start-datetime', type=str, required=True,
                   help='-s option are required, eg:"2022-04-21 14:00:00"')
parse.add_argument('-c', '--copied-sector-number', type=int, required=True, help='-c option are required')
args = parse.parse_args()

try:
    diff_hour = (time.time() - time.mktime(time.strptime(args.start_datetime, "%Y-%m-%d %H:%M:%S"))) / 3600
    finish_parent = args.copied_sector_number / args.total_number * 100
    need_days = args.total_number / (args.copied_sector_number / diff_hour) / 24
    finish_timestamp = time.mktime(time.strptime(args.start_datetime, "%Y-%m-%d %H:%M:%S")) + need_days * 3600 * 24
    finish_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(finish_timestamp))
    print(f"已完成{round(finish_parent, 2)}%，预计需要{round(need_days, 2)}天，大概在{finish_datetime}迁移完成。")
except Exception as err:
    print(err)
    print(parse.print_help())
