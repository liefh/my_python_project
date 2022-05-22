# import requests,time
# from bs4 import BeautifulSoup
#
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }
#
# url_dict = {
#     'pmp_part_1':'https://pili-vods.huixiangtiandi.com/custom/huixiang/undefined/20200323233634.mp4',
#     'pmp_part_2':'https://pili-vods.huixiangtiandi.com/custom/huixiang/undefined/20200323234329.mp4',
#     'pmp_part_3':'https://pili-vods.huixiangtiandi.com/custom/huixiang/undefined/20200328215525.mp4',
#     'pmp_part_4':'https://pili-vods.huixiangtiandi.com/custom/huixiang/undefined/20200328221535.mp4',
#     'pmp_part_5':'https://pili-vods.huixiangtiandi.com/custom/huixiang/undefined/202003310140.mp4',
#     'pmp_part_6':'https://pili-vods.huixiangtiandi.com/custom/huixiang/undefined/202003310434.mp4',
# }
#
# for name,url in url_dict.items():
#     print(name,url)
#     context = requests.get(url,headers=headers)
#     soup = BeautifulSoup(context.text,'lxml')
#     data_obj = soup.select('body > video > source')
#     for data_item in data_obj:
#         data = data_item.get_text()
#         with open(f'./datas/{name}.mp4','wb+') as wf:
#             wf.write(data)
#             wf.flush()
#             wf.close()
#
#     time.sleep(5)


# import  subprocess,paramiko,xlsxwriter
#
# workbook = xlsxwriter.Workbook('xj_test.xlsx')
# worksheet = workbook.add_worksheet('xj')
# worksheet.write(0,0,"IP")
# worksheet.write(0,1,"CPU")
# worksheet.write(0,2,"MeM")
# worksheet.write(0,3,"GPU")
#
# worksheet.write(1,0,"1.1.1.1")
# worksheet.write(1,2,"amd")
# worksheet.write(1,3,"2TiB")
# worksheet.write(1,1,"2080")
# workbook.close()

# import  subprocess,paramiko,xlwt,xlrd
# import paramiko, xlsxwriter
#
# # ip_list = ['172.26.12.112','172.26.12.113']
# ip_list = [
#     '172.26.13.111',
#     '172.26.13.112',
#     '172.26.13.113',
#     '172.26.13.114',
#     '172.26.13.115',
#     '172.26.13.116',
#     '172.26.13.121',
#     '172.26.13.122',
#     '172.26.13.123',
#     '172.26.13.124',
#     '172.26.13.125',
#     '172.26.13.126',
#     '172.26.13.131',
#     '172.26.13.132',
#    ]
# port = 62534
#
# shell_cpu = "lscpu | grep 'Model name:' | awk  -F ':' '{print $NF}'"
# shell_mem = "free -lh |grep 'Mem:' | awk '{print $2}'"
# shell_gpu = "nvidia-smi -L"
#
# pkey = '/root/.ssh/id_rsa'
# key = paramiko.RSAKey.from_private_key_file(pkey)
#
# workbook = xlsxwriter.Workbook('xj服务器.xlsx')
# worksheet = workbook.add_worksheet('xj')
# worksheet.write(0, 0, "IP")
# worksheet.write(0, 1, "CPU")
# worksheet.write(0, 2, "MeM")
# worksheet.write(0, 3, "GPU")
#
# row_num = 1
# for ip in ip_list:
#     print(ip)
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
#     ssh.connect(hostname=ip, port=port, username='root', pkey=key, timeout=3, auth_timeout=3)
#     stdin, stdout, stderr = ssh.exec_command(shell_cpu)
#     result_cpu = stdout.readlines()[0].strip()
#
#     stdin, stdout, stderr = ssh.exec_command(shell_mem)
#     result_mem = stdout.readlines()[0].strip()
#
#     stdin, stdout, stderr = ssh.exec_command(shell_gpu)
#     result_gpu=''
#     for gpu_content in stdout.readlines():
#         result_gpu = gpu_content.strip().strip('\n') + ';' + result_gpu
#
#     worksheet.write(row_num, 0, ip)
#     worksheet.write(row_num, 1, result_cpu)
#     worksheet.write(row_num, 2, result_mem)
#     worksheet.write(row_num, 3, result_gpu)
#
#     print(row_num, ip, result_cpu, result_mem, result_gpu)
#     ssh.close()
#     row_num += 1
#
# workbook.close()
# print('finished')



# str_1 = 'adc'
# int_1 = 111
# dict_1 = {'a':'a','b':111}
# ip_1 = '192.168.1.1'
# ip_2 = '192.168.1.2'
# print(hash(str_1))
# print(hash(int_1))
# # print(hash(dict_1))
# print(hash(ip_1))
# print(hash(ip_2))
#
# #
# url = 'rm-wz9g396hofh020yd5mo.mysql.rds.aliyuncs.com'
# port = 3306
# user = 'ipfs'
# passwd = 'Ipfs@123'
# db_name = 'lotus'
# #
# #
# #
# def connect_mysql(url, port, user, passwd, db_name):
#     import pymysql
#     try:
#         connect = pymysql.connect(host=url, port=port, user=user, passwd=passwd, db=db_name)
#         cursor = connect.cursor(pymysql.cursors.DictCursor)
#         cursor.execute('SELECT VERSION();')
#         result = cursor.fetchone()
#         if result:
#             print('mysql connect successfully!')
#         return cursor
#     except Exception as err:
#         print('mysql connect failed!')
#         print(err)
#         exit(-3)
#
#
# def date_uncompress_zlib(date_compressed):
#     import zlib, json
#     if not date_compressed:
#         print('The string of decompressed is none!')
#         exit(-2)
#     decompress_obj = zlib.decompressobj()
#     data_binary = decompress_obj.decompress(date_compressed)
#     # return a dict
#     return json.loads(data_binary)
# #
# #
# # cursor = connect_mysql(url=url, port=port, user=user, passwd=passwd, db_name=db_name)
# # sql = 'SELECT params from task_params where task_id=5106639 ;'
# #
# # cursor.execute(sql)
# # params_fetch_list = cursor.fetchall()
# #
# # for params_fetch in params_fetch_list:
# #     print(params_fetch)
# #     params_compressed = params_fetch['params']
# #     date_decompressed = date_uncompress_zlib(params_compressed)
# #     print(date_decompressed)
# #     print(params_compressed)
# # print(type(params_compressed))
# #
# #
# s1= bytes("{'cacheDir': 'cache/s-t01022733-254832', 'sealedPath': 'sealed/s-t01022733-254832', 'remoteSealedDir': '/mnt/qn/sealed', 'remoteCacheDir': '/mnt/qn/cache/s-t01022733-254832'}")
# #
# #
# import zlib,pymysql
# compress = zlib.compress(s1)
# print(compress)
# print('-0-----------------')
# date_decompressed = date_uncompress_zlib(compress)
# print(date_decompressed)
#     # print(params_compressed)
#
#
#
#
# connect = pymysql.connect(host=url, port=port, user=user, passwd=passwd, db=db_name)
# cursor = connect.cursor(pymysql.cursors.DictCursor)
# sql = F'update task_params set params={compress} where task_id=5106639;'
# cursor = connect_mysql(url=url, port=port, user=user, passwd=passwd, db_name=db_name)
# print(sql)
# print(cursor.execute('UPDATE task_params set params = %s where task_id=5106639',compress))
# connect.commit()
#
#
#
#
#
#
#
# # result_uncompressed =  date_uncompress_zlib(params_fetch)
# # print(result_uncompressed,type(result_uncompressed))
#
#
# # print(params_fetch,type(params_fetch))
# #
# # import json
# # for params_compressed in params_fetch:
# #     # print(i)
# #     print(params_compressed,type(params_compressed))
# #     # params_compressed = params_fetch['params']
# #     # print(params_compressed,type(params_compressed))
# #     # date_decompressed = date_uncompress_zlib(params_compressed)
# #     # print(date_decompressed)
# #     # result = {'sector_id': sector_id, 'ticket': date_decompressed['ticket'], 'seed': date_decompressed['seed']}
# #     # print(result)
# #     # with open('./ticket_seed.json', 'a+') as f:
# #     #     json.dump(result, f)
# #     #     f.write(',')
# #
# #     # print(i)

# times = 999999999999
# times = 100000000000
# result = (1+1/times)**times
# print(result)
# import math
# print(math.exp(1))

# times = 12
# sum,tmp = 1,1
# for i in range(1,times+1):
#     tmp *=i
#     sum += 1/tmp
# print(sum)

# import json, requests, sys
#
# headers = {'Content-Type': 'application/json;charset=utf-8'}
# data = {
#     'msgtype': 'text',
#     'text': {
#         'content': '唵嘛呢叭咪吽'
#     }
# }
#
# ding_url = 'https://oapi.dingtalk.com/robot/send?access_token=5a68f614b3a9ba9b8d362f6ce3d2d7f496f6735813fc34ed34826ad7fb196047'
#
# req = requests.post(url=ding_url, headers=headers, data=json.dumps(data))
# print(req)

# import requests, json
# from bs4 import  BeautifulSoup
# # https://www.aleo.network/leaderboard/aleo1trnczew3y95uka8zwtnqt9c8u8wtsh8xxg5s6zh0vn8jtgg96uyqrac55e
# site_url = 'https://www.aleo.network/leaderboard/aleo1trnczew3y95uka8zwtnqt9c8u8wtsh8xxg5s6zh0vn8jtgg96uyqrac55e'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
# }
# content = requests.get(url=site_url, headers=headers, timeout=(5, 10))
# context = content.text
# print(context)
# data_dic = json.loads(context)

