import  zlib,json
#
# with open('./datas/params','rb') as in_f:
#     data_b = in_f.read()
#
#     decompress = zlib.decompressobj()
#     data = decompress.decompress(data_b)
#     print(data)


import  pymysql
# url = 'rm-8vbz2h506pc2n324b7o.mysql.zhangbei.rds.aliyuncs.com'
url = 'rm-8vbz2h506pc2n324b7o.mysql.zhangbei.rds.aliyuncs.com'
db = 'lotus-bak'
user='ipfs'
passwd = 'Ipfs@123'


connect = pymysql.connect(host=url,port=3306,user=user,passwd=passwd,db=db,)
cursor =connect.cursor(pymysql.cursors.DictCursor)


with open('datas/f020330-sectorid.log','r') as rf:
    for line in rf:
        print(line)
        sector_id = int(line)
        sql = f'SELECT sector_id,params from task_params where task_id in (SELECT id FROM tasks WHERE task_type=4 and sector_id in ({sector_id}));'
        # print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)

        for data_de in results:
            # sector_id = data_de['sector_id']
            params = data_de['params']
            decompress = zlib.decompressobj()
            data = decompress.decompress(params)
            result = json.loads(data)
            result_dict = {'sector_id': sector_id, 'ticket': result['ticket'], 'seed': result['seed']}
            print(result_dict)
            with open('datas/wl01_lotus_bak.json', 'a+') as f:
                json.dump(result_dict,f)
                json.dump(',',f)



connect.close()
