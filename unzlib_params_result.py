import pymysql

database_url = 'rm-wz93e6t74so51xk89so.mysql.rds.aliyuncs.com'
database_port = 3306
database_user = 'ipfs'
database_password = 'Ipfs@123'
database_name = 'lotus_recover'

task_type = 16
sector_id = 14092

def date_uncompress_zlib(date_compressed):
    import zlib, json
    if not date_compressed:
        print('The string of decompressed is none!')
        exit(-2)
    decompress_obj = zlib.decompressobj()
    data_binary = decompress_obj.decompress(date_compressed)
    # return a dict
    return json.loads(data_binary)

connect = pymysql.connect(host=database_url, port=database_port, user=database_user, passwd=database_password, db=database_name)
cursor = connect.cursor(pymysql.cursors.DictCursor)
sql = f'SELECT params,result from task_params where task_id in (SELECT id FROM tasks WHERE task_type={task_type} and sector_id={sector_id});'
cursor.execute(sql)
data_fetch = cursor.fetchone()
params_compressed = data_fetch['params']
result_compressed = data_fetch['result']

params_decompressed = date_uncompress_zlib(params_compressed)
result_decompressed = date_uncompress_zlib(params_compressed)

print(params_decompressed)


