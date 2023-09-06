def get_cmdb_token(cmdb_token_api):
    import requests
    token_header = {
        'Content-Type':'application/json'
    }

    token_raw = {
        'username': 'wenzhong',
        'password': '123456'
    }

    cmdb_token = requests.post(url=cmdb_token_api,headers=token_header,json=token_raw).json()['token']

    return cmdb_token



def get_cmdb_servers_miner(cmdb_api):
    import requests
    cmdb_token = get_cmdb_token('http://47.98.223.69/api/v1/token')

    try:
        cmdb_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Authorization': f'JWT {cmdb_token}',
            # 'Cookie': 'csrftoken=tUEHSKREqJL9roNllYa8VBEZMjzqDzg6wAeg9bF6oAKRhdnxd3Etm5XjRIwpHMc3',
            'Content - Type': 'application/json'
        }
        cmdb_payload = {"indices": ["servers_miner"], "query": "*", "page": 1, "page_size": 10000, "width": True}

        cmdb_servers_miner = list()

        cmdb_response = requests.post(url=cmdb_api, headers=cmdb_headers, json=cmdb_payload).json()
        # print(cmdb_response)

        for cmdb_response_servers_miner in cmdb_response['hits']:
            cmdb_server_miner = cmdb_response_servers_miner['_source']
            cmdb_server_miner['_id'] = cmdb_response_servers_miner['_id']
            cmdb_servers_miner.append(cmdb_server_miner)

    except Exception as e:
        print(e)
        exit(3)

    return cmdb_servers_miner


def delete_cmdb(cmdb_delete_api, delete_data):
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
    cmdb_list_api = 'http://47.98.223.69/api/v1/search/data-lucene'
    cmdb_delete_api = 'http://47.98.223.69/api/v1/data/servers_miner'


    cmdb_servers_miner=get_cmdb_servers_miner(cmdb_list_api)


    # # ## 删除cmdb servers_info表所有数据
    for delete_data in cmdb_servers_miner:
        delete_cmdb(cmdb_delete_api,delete_data['_id'])




