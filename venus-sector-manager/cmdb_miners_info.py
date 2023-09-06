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



def get_cmdb_infos(cmdb_api_list,cmdb_table_name):
    import requests
    cmdb_token = get_cmdb_token('http://47.98.223.69/api/v1/token')

    try:
        cmdb_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Authorization': f'JWT {cmdb_token}',
            # 'Cookie': 'csrftoken=tUEHSKREqJL9roNllYa8VBEZMjzqDzg6wAeg9bF6oAKRhdnxd3Etm5XjRIwpHMc3',
            'Content - Type': 'application/json'
        }
        cmdb_payload = {"indices": [cmdb_table_name], "query": "*", "page": 1, "page_size": 10000, "width": True}

        cmdb_infos = list()

        cmdb_response = requests.post(url=cmdb_api_list, headers=cmdb_headers, json=cmdb_payload).json()
        # print(cmdb_response)

        for cmdb_response_info in cmdb_response['hits']:
            cmdb_info = cmdb_response_info['_source']
            cmdb_info['_id'] = cmdb_response_info['_id']
            cmdb_infos.append(cmdb_info)

    except Exception as e:
        print(e)
        exit(3)

    return cmdb_infos


def delete_cmdb_info(cmdb_delete_api,cmdb_table_name, cmdb_info_id):
    import requests
    cmdb_token = get_cmdb_token('http://47.98.223.69/api/v1/token')
    cmdb_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Authorization': f'JWT {cmdb_token}',
        'Content - Type': 'application/json'
    }

    cmdb_delete_api = cmdb_delete_api + '/' + cmdb_table_name + '/' + cmdb_info_id
    # print(cmdb_delete_api)

    try:
        cmdb_delete_response = requests.delete(url=cmdb_delete_api, headers=cmdb_headers)

    except Exception as e:
        print(e)
        exit(3)




if __name__ == '__main__':
    cmdb_list_api = 'http://47.98.223.69/api/v1/search/data-lucene'
    cmdb_delete_api = 'http://47.98.223.69/api/v1/data'


    cmdb_infos=get_cmdb_infos(cmdb_list_api,cmdb_table_name='miners_info')
    # print(cmdb_infos)


    # # ## 删除cmdb servers_info表所有数据
    for cmdb_info in cmdb_infos:
        delete_cmdb_info(cmdb_delete_api,cmdb_table_name='miners_info',cmdb_info_id=cmdb_info['_id'])




