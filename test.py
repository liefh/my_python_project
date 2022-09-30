# a = [4,5,7,8,9,9,9,9]
# s = list()
# for i in range(0,len(a),2):
#     b = a[i:i+4]
#     print(b)
#     s.append(b)
#
#
# print(s)


# import  time
# print(time.time())
# print(time.localtime())
# print(time.localtime(time.time()))
# print()time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime(time.time()))



import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%SZ',
                    filemode='a')
logger = logging.getLogger()
logger.info('fdsa  fdafd fdfdds')


