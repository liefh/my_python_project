# from pathlib import Path
import toml, pymysql, zlib, json

sectors_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


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
    # finally:
    #     connect.close()

def date_uncompress_zlib(date_compressed):
    import zlib,json
    if not date_compressed:
        print('The string of decompressed is none!')
        exit(-4)
    decompress_obj = zlib.decompressobj()
    data_binary = decompress_obj.decompress(date_compressed)
    return json.loads(data_binary)


config_dict = read_config_toml('datas/databases.toml')
# print(config_dict)
cursor = connect_mysql(url=config_dict['url'], port=config_dict['port'], user=config_dict['user'],
                       passwd=config_dict['passwd'],
                       db_name=config_dict['db_name'])

for sector_id in sectors_id:
    sql = f'SELECT params from task_params where task_id in (SELECT id FROM tasks WHERE task_type=4 and sector_id in ({sector_id}));'
    # print(sql)
    cursor.execute(sql)
    params_fetch = cursor.fetchone()
    params_compressed = params_fetch['params']
    date_decompressed = date_uncompress_zlib(params_compressed)
    result = {'sector_id': sector_id, 'ticket': date_decompressed['ticket'], 'seed': date_decompressed['seed']}


cursor.close()
