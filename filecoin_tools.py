import time
import argparse, sys

function_dict = {
    'epoch_to_datetime': ['epoch'],
    'datetime_to_epoch': ['datetime'],
    'sectors_group': ['sectors_file', 'group_count', 'start_group_id', 'sectors_groups_file'],
}


def epoch_to_datetime(epoch):
    # geneses_epoch = 0
    # geneses_datetime = '2020-08-25 06:00:00'
    geneses_timestamp = 1598306400
    epoch_timestamp = geneses_timestamp + epoch * 30
    epoch_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epoch_timestamp))
    return epoch_datetime


def datetime_to_epoch(my_datetime):
    # geneses_epoch = 0
    # geneses_datetime = '2020-08-25 06:00:00'
    geneses_timestamp = 1598306400
    my_timestamp = time.mktime(time.strptime(my_datetime, "%Y-%m-%d %H:%M:%S"))
    my_epoch = int((my_timestamp - geneses_timestamp) / 30)
    return my_epoch


def sectors_group_by_group(sectors_file, group_count, start_group_id, sectors_groups_file):
    import math
    with open(f'{sectors_file}') as rf:
        sectors_id = list()
        for sector_id in rf:
            sector_id = int(sector_id.strip())
            sectors_id.append(sector_id)
            sectors_id.sort()

    sectors_per_group = math.ceil(len(sectors_id) / group_count)

    with open(f'{sectors_groups_file}', 'wt') as wf:
        group_id = start_group_id
        for group in range(0, len(sectors_id), sectors_per_group):
            tmp_list = sectors_id[group:group + sectors_per_group]
            print(
                f'UPDATE task_groups SET group_id={group_id} WHERE sector_id BETWEEN {tmp_list[0]} AND {tmp_list[-1]};')
            for sector_id in tmp_list:
                wf.write(f'UPDATE task_groups SET group_id={group_id} WHERE sector_id={sector_id};')
                wf.write('\n')
            group_id = group_id + 1
        wf.flush()


def sectors_group_by_sector(sectors_file, sector_number, start_group_id, sectors_groups_file):
    import math
    with open(f'{sectors_file}') as rf:
        sectors_id = list()
        for sector_id in rf:
            sector_id = int(sector_id.strip())
            sectors_id.append(sector_id)
            sectors_id.sort()

    sectors_per_group = sector_number

    with open(f'{sectors_groups_file}', 'wt') as wf:
        group_id = start_group_id
        for group in range(0, len(sectors_id), sectors_per_group):
            tmp_list = sectors_id[group:group + sectors_per_group]
            print(
                f'UPDATE task_groups SET group_id={group_id} WHERE sector_id BETWEEN {tmp_list[0]} AND {tmp_list[-1]};')
            for sector_id in tmp_list:
                wf.write(f'UPDATE task_groups SET group_id={group_id} WHERE sector_id={sector_id};')
                wf.write('\n')
            group_id = group_id + 1
        wf.flush()


parser = argparse.ArgumentParser()

# add subparse : epoch_to_datetime
subparser_epoch_to_datetime = subparsers.add_parser('epoch_to_datetime', help='epoch is converted to datetime')
subparser_epoch_to_datetime.add_argument('-e', '--epoch', type=int, help='epoch is converted to datetime')
subparser_epoch_to_datetime.set_defaults(function=epoch_to_datetime)

# add subparse : datetime_to_epoch
subparser_datetime_to_epoch = subparsers.add_parser('datetime_to_epoch', help='datetime is converted to epoch')
subparser_datetime_to_epoch.add_argument('-d', '--datetime', type=str, help='datetime is converted to epoch')
subparser_datetime_to_epoch.set_defaults(function=datetime_to_epoch)

# add subparse : sectors_group
subparser_sectors_group = subparsers.add_parser('sectors_group', help='sectors were divided into groups averagely')
subparser_sectors_group.add_argument('-i', '--input_file', type=str, help='input a file containing only sectors')
subparser_sectors_group.add_argument('-g', '--group_count', type=int, help='group count')
subparser_sectors_group.add_argument('-n', '--sector_number', type=int, help='group count')
subparser_sectors_group.add_argument('-s', '--start_group_id', type=int, help='start group id')
subparser_sectors_group.add_argument('-o', '--output_file', type=str,
                                     help='output a file contained sector_id and group_id')
args = parser.parse_args()
if args.group_count:
    subparser_sectors_group.set_defaults(function=sectors_group_by_group)

if args.sector_number:
    subparser_sectors_group.set_defaults(function=sectors_group_by_sector)
args = parser.parse_args()

try:
    if not hasattr(args, 'function'):
        print(parser.print_usage())
        exit(3)

    if getattr(args, 'function') == epoch_to_datetime:
        print(epoch_to_datetime(args.epoch))

    if getattr(args, 'function') == datetime_to_epoch:
        print(datetime_to_epoch(args.datetime))

    if getattr(args, 'function') == sectors_group_by_group:
        print(sectors_group_by_group(args.input_file, args.group_count, args.start_group_id, args.output_file))

    if getattr(args, 'function') == sectors_group_by_sector:
        print(sectors_group_by_sector(args.input_file, args.sector_number, args.start_group_id, args.output_file))

except Exception as err:
    print(parser.print_usage())
    print(err)
    exit(33)
