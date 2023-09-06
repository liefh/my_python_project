from typing import List, Any


def get_prom_servers_info(prom_url, prom_query):
    from prometheus_api_client import PrometheusConnect

    prom_url = prom_url
    prom_query = prom_query

    pop_keys = ['job']
    prom_servers_info = list()

    try:
        prom_conn = PrometheusConnect(url=prom_url)
        query_result = prom_conn.custom_query(prom_query)

        for server_metirc in query_result:
            server_info = server_metirc['metric']
            [server_info.pop(pop_key) for pop_key in pop_keys]
            server_info['instance'] = server_info['instance'].split(':')[0]
            server_info['product'] = server_info['product'].strip(',')
            prom_servers_info.append(server_info)

    except Exception as e:
        print(e)
        print('获取prometheus信息失败！')
        exit(3)
    # print(prom_servers_info)
    return prom_servers_info


def get_cmdb_token(cmdb_token_api):
    import requests
    token_header = {
        'Content-Type': 'application/json'
    }

    token_raw = {
        'username': 'wenzhong',
        'password': '123456'
    }

    cmdb_token = requests.post(url=cmdb_token_api, headers=token_header, json=token_raw).json()['token']

    return cmdb_token


def get_cmdb_servers_info(cmdb_api):
    import requests
    cmdb_token = get_cmdb_token('http://47.98.223.69/api/v1/token')

    try:
        cmdb_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Authorization': f'JWT {cmdb_token}',
            # 'Cookie': 'csrftoken=tUEHSKREqJL9roNllYa8VBEZMjzqDzg6wAeg9bF6oAKRhdnxd3Etm5XjRIwpHMc3',
            'Content - Type': 'application/json'
        }
        cmdb_payload = {"indices": ["servers_info"], "query": "*", "page": 1, "page_size": 10000, "width": True}

        cmdb_response = requests.post(url=cmdb_api, headers=cmdb_headers, json=cmdb_payload).json()
        # print(cmdb_response)

        for cmdb_response_server_info in cmdb_response['hits']:
            cmdb_server_info = cmdb_response_server_info['_source']
            cmdb_server_info['_id'] = cmdb_response_server_info['_id']
            # print(cmdb_response_server_info)
            # print(cmdb_server_info)
            # print(cmdb_server_info)
            # print(cmdb_server_info)
            # cmdb_server_info['__id']=cmdb_server_info['_id']
            cmdb_servers_info.append(cmdb_server_info)

    except Exception as e:
        print(e)
        exit(3)

    return cmdb_servers_info


def insert_cmdb_servers_info(cmdb_update_api, update_data):
    import requests
    cmdb_token = get_cmdb_token('http://47.98.223.69/api/v1/token')
    cmdb_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Authorization': f'JWT {cmdb_token}',
        'Content - Type': 'application/json'
    }

    try:
        cmdb_update_response = requests.post(url=cmdb_update_api, headers=cmdb_headers, data=update_data)

    except Exception as e:
        print(e)
        exit(3)


def delete_cmdb_servers_info(cmdb_delete_api, delete_data):
    import requests
    cmdb_token = get_cmdb_token('http://47.98.223.69/api/v1/token')
    cmdb_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Authorization': f'JWT {cmdb_token}',
        'Content - Type': 'application/json'
    }

    cmdb_delete_api = cmdb_delete_api + '/' + delete_data

    try:
        cmdb_update_response = requests.delete(url=cmdb_delete_api, headers=cmdb_headers)

    except Exception as e:
        print(e)
        exit(3)


if __name__ == '__main__':
    prom_url = 'http://139.196.147.220:9090'
    prom_query = 'sum_over_time(up{uuid!=""}[10m])>=5'
    cmdb_list_api = 'http://47.98.223.69/api/v1/search/data-lucene'
    cmdb_insert_api = 'http://47.98.223.69/api/v1/data/servers_info'
    cmdb_delete_api = 'http://47.98.223.69/api/v1/data/servers_info'

    prom_servers_info = get_prom_servers_info(prom_url, prom_query)

    cmdb_servers_info = get_cmdb_servers_info(cmdb_list_api)
    # print(cmdb_servers_info)

    # cmdb_servers_uuid = [cmdb_server_info['uuid'] for cmdb_server_info in cmdb_servers_info]
    cmdb_servers_uuid = list(cmdb_server_info['uuid'] for cmdb_server_info in cmdb_servers_info)

    # # # ## 删除cmdb servers_info表所有数据
    # for cmdb_server_info in cmdb_servers_info:
    #     delete_cmdb_servers_info(cmdb_delete_api,cmdb_server_info['_id'])

    ## 插入prometheus 到 cmdb
    for prom_server_info in prom_servers_info:
        if prom_server_info['uuid'] not in cmdb_servers_uuid:
            insert_cmdb_servers_info(cmdb_insert_api, prom_server_info)
            print(f'cmdb插入 {prom_server_info} 成功')
            continue
        print(f'cmdb中已存在 {prom_server_info}')
