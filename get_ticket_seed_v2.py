"""
exit(-1): file not exist;
exit(-2): content of file or data of input is none;
exit(-3): mysql connect error;
"""


def create_sample_file():
    with open('./databases_sample.toml', 'wt') as wf:
        wf.write('# This is a sample config file.\n')
        wf.write('[mysql_service]\n')
        wf.write("url = '1.2.3.4'\n")
        wf.write('port = 3306\n')
        wf.write("user = 'my_name'\n")
        wf.write("passwd = 'my_passwd'\n")
        wf.write("db_name = 'my_db'\n")
        wf.flush()


def read_config_toml(file_path):
    from pathlib import Path
    import toml
    path = Path(file_path)
    if not path.exists():
        print('databases.toml is not exist')
        exit(-1)

    config = toml.load(file_path)

    if not config['mysql_service']:
        print('config file is none,please check databases.toml')
        exit(-2)

    return config['mysql_service']


def connect_mysql(url, port, user, passwd, db_name):
    import pymysql
    try:
        connect = pymysql.connect(host=url, port=port, user=user, passwd=passwd, db=db_name)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT VERSION();')
        result = cursor.fetchone()
        if result:
            print('mysql connect successfully!')
        return cursor
    except Exception as err:
        print('mysql connect failed!')
        print(err)
        exit(-3)


def date_uncompress_zlib(date_compressed):
    import zlib, json
    if not date_compressed:
        print('The string of decompressed is none!')
        exit(-2)
    decompress_obj = zlib.decompressobj()
    data_binary = decompress_obj.decompress(date_compressed)
    # return a dict
    return json.loads(data_binary)


if __name__ == '__main__':
    import json
    from pathlib import Path

    create_sample_file()

    path = Path('./sectors_id')
    if not path.exists():
        print('The file is not existed, Please create sectors_id file in current directory.')
        exit(-1)
    if path.stat().st_size == 0:
        print('The sectors_id file is none, make sure include all sector id in sectors_id file.')
        exit(-2)

    path = Path('./ticket_seed.json')
    path.touch(exist_ok=True)
    path.unlink()
    path.touch()

    config_dict = read_config_toml('./databases.toml')

    cursor = connect_mysql(url=config_dict['url'],
                           port=int(config_dict['port']),
                           user=config_dict['user'],
                           passwd=config_dict['passwd'],
                           db_name=config_dict['db_name'])

    with open('./sectors_id', 'r') as rf:
        for sector_id in rf:
            sector_id = sector_id.strip()
            sql = f'SELECT result from task_params where task_id in (SELECT id FROM tasks WHERE task_type=2 and sector_id={sector_id});'
            # print(sql)
            cursor.execute(sql)
            params_fetch = cursor.fetchone()
            print(params_fetch)
            params_compressed = params_fetch['result']
            date_decompressed = date_uncompress_zlib(params_compressed)
            print(date_decompressed)
            result = {'sector_id': sector_id, 'ticket': date_decompressed['ticket'], 'seed': date_decompressed['seed']}
            print(result)
            with open('./ticket_seed.json', 'a+') as f:
                json.dump(result, f)
                f.write(',')

    cursor.close()
