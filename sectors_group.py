
def sectors_group(sectors_file,group_count,start_group_id,sectors_groups_file):
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

sectors_group('./sectors_id',6,10001,'./sectors_group')