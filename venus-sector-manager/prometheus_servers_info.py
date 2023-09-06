import requests
import json

prom_servers_info = list()

from prometheus_api_client import PrometheusConnect


# 连接到 Prometheus
prometheus_url = 'http://139.196.147.220:9090'

prom = PrometheusConnect(url=prometheus_url)

# 定义查询语句
query = 'sum_over_time(up{uuid!=""}[10m]) > 30'

# 发送查询请求
prom_data = prom.custom_query(query)

# 处理响应
for result in prom_data:
    metric = result['metric']
    pop_keys = ['job']
    [metric.pop(pop_key) for pop_key in pop_keys]
    metric['instance'] = metric['instance'].split(':')[0]
    metric['product'] = metric['product'].strip(',')
    prom_servers_info.append(metric)
# print(prom_servers_info)

# cmdb_url = 'http://47.98.223.69/api/v1'
cmdb_url = 'http://47.98.223.69/api/v1/data/servers_info'
headers = {'Authorization':'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6Indlbnpob25nIiwiZXhwIjoxNjgyMDU1NDk0LCJlbWFpbCI6Indlbnpob25nQGt1bnlhb2tlamkuY29tIn0.jlLSqKIPX_kbROimPly5WoP14HEGZvzq4iHJpUhbC1A',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Cookie':'csrftoken=PJBsJkzQTvfO0TjHWamFXY8FkWdiOYyVjr3GeuNdxkFkHj9PsPQiH7CiIvR1uuWQ; sessionid=aivg4aghju8fec60iu8vymlkxjes8c91'
           }
cmdb_response = requests.get(url=cmdb_url,headers=headers)
cmdb_servers_uuid = list()
for uuid in json.loads(cmdb_response.text)['hits']:
    cmdb_servers_uuid.append(uuid['_source']['uuid'])
# print(cmdb_servers_uuid)









# 对比prometheus和cmdb，更新cmdb
for prometheus_server_info in prom_servers_info:
    if prometheus_server_info['uuid'] not in cmdb_servers_uuid:
        cmdb_response = requests.post(url=cmdb_url,headers=headers,data=prometheus_server_info)
        print(f'cmdb插入输入：{prometheus_server_info}')
        continue
    print('资源无变更')
