import logging
import requests
from prometheus_api_client import PrometheusConnect


logging.basicConfig(
    # filename='xxx',
    # filemode='a',
    # encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s %(filename)s %(funcName)s[line:%(lineno)d]',
    datefmt="%FT%T",
)

def prom_get_servers_info(prom_url, prom_query):

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
        logging.info('prometheus 获取数据成功')
        return prom_servers_info

    except Exception as e:
        logging.error('prometheus 获取数据失败')
        logging.error(f'prometheus 获取数据错误 : {e}')



class cmdbTableDataOperate():

    cmdb_api = ''

    def __init__(self,cmdb_table_name,record_data=None):
        self.cmdb_table_name = cmdb_table_name
        self.record_data = record_data


    def cmdb_get_headers(self):
        cmdb_token_api = cmdb_api + '/' + 'token'
        import requests
        token_header = {
            'Content-Type': 'application/json'
        }

        token_raw = {
            'username': 'wenzhong',
            'password': '123456'
        }

        try:
            cmdb_token_response = requests.post(url=cmdb_token_api, headers=token_header, json=token_raw)

            if cmdb_token_response.status_code != 200:
                logging.error('cmdb token获取失败')
                return 3
            cmdb_token = cmdb_token_response.json()['token']
            cmdb_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                'Authorization': f'JWT {cmdb_token}',
                'Content - Type': 'application/json'
            }
            logging.info('cmdb token获取成功')
            logging.debug(f'cmdb headers值为 : {cmdb_headers}')
            return cmdb_headers

        except Exception as e:
            logging.error(f'cmdb获取token错误 : {e}')




    def insert_record(self,record_data):
        cmdb_search_data_api = cmdb_api + '/' + 'search/data-lucene'
        cmdb_operate_data_api = cmdb_api + '/' + 'data' + '/' + f'{self.cmdb_table_name}'

        try:
            cmdb_insert_response = requests.post(url=cmdb_operate_data_api, headers=self.cmdb_get_headers(), data=record_data)
            if cmdb_insert_response.status_code != 201:
                logging.error(f'cmdb 记录写入错误 {record_data}')
                return 3

            logging.info(f'cmdb 记录写入成功 {record_data}')
            return 0


        except Exception as e:
            logging.error(f'cmdb插入数据错误 : {e}')

    def get_table_records(self):
        cmdb_search_data_api = cmdb_api + '/' + 'search/data-lucene'
        cmdb_operate_data_api = cmdb_api + '/' + 'data' + '/' + f'{self.cmdb_table_name}'
        cmdb_payload = {"indices": [f"{self.cmdb_table_name}"], "query": "*", "page": 1, "page_size": 10000, "width": True}
        cmdb_table_records = []
        try:
            cmdb_get_response = requests.post(url=cmdb_search_data_api, headers=self.cmdb_get_headers(), json=cmdb_payload)
            if cmdb_get_response.status_code != 200:
                logging.info(f'cmdb 表获取数据失败')
                return 3
            cmdb_response_records_data = cmdb_get_response.json()
            for cmdb_response_record_data in cmdb_response_records_data['hits']:
                cmdb_record_data = cmdb_response_record_data['_source']
                cmdb_record_data['_id'] = cmdb_response_record_data['_id']
                cmdb_table_records.append(cmdb_record_data)

            logging.info(f'cmdb 表获取数据成功 {self.cmdb_table_name}')
            return cmdb_table_records

        except Exception as e:
            logging.error(f'cmdb 表获取数据错误 : {e}')

    def delete_table_records(self):
        cmdb_search_data_api = cmdb_api + '/' + 'search/data-lucene'
        cmdb_operate_data_api = cmdb_api + '/' + 'data' + '/' + f'{self.cmdb_table_name}'
        cmdb_payload = {"indices": [f"{self.cmdb_table_name}"], "query": "*", "page": 1, "page_size": 10000,
                        "width": True}
        cmdb_table_records = []
        try:
            cmdb_get_response = requests.post(url=cmdb_search_data_api, headers=self.cmdb_get_headers(),
                                              json=cmdb_payload)
            if cmdb_get_response.status_code != 200:
                logging.info(f'cmdb 获取数据失败')
                return 3
            cmdb_response_records_data = cmdb_get_response.json()
            headers = self.cmdb_get_headers()
            for cmdb_response_record_data in cmdb_response_records_data['hits']:
                cmdb_record_data = cmdb_response_record_data['_source']
                cmdb_record_data['_id'] = cmdb_response_record_data['_id']
                cmdb_table_records.append(cmdb_record_data)
                cmdb_operate_data_api = cmdb_api + '/' + 'data' + '/' + f'{self.cmdb_table_name}' + '/' + cmdb_response_record_data['_id']
                cmdb_delete_response = requests.delete(url=cmdb_operate_data_api, headers=headers)
                if cmdb_delete_response.status_code != 204:
                    logging.error(f'cmdb 记录删除失败 {self.record_data}')
                    return 3
                logging.debug(f'cmdb 记录删除成功 {self.record_data}')

            logging.info(f'cmdb 表删除成功 {self.cmdb_table_name}')
            return 0

        except Exception as e:
            logging.error(f'cmdb 删除表错误 : {e}')



if __name__ == '__main__':
    prom_url = 'http://139.196.147.220:9090'
    prom_query = 'sum_over_time(up{uuid!=""}[10m])>=5'

    cmdb_api = 'http://47.98.223.69/api/v1'
    cmdbTableDataOperate.cmdb_api=cmdb_api

    cmdb_servers_info = cmdbTableDataOperate(cmdb_table_name='servers_info')
    cmdb_servers_info.delete_table_records()

    cmdb_servers_miner = cmdbTableDataOperate(cmdb_table_name='servers_miner')
    cmdb_servers_miner.delete_table_records()


    prom_datas = prom_get_servers_info(prom_url=prom_url,prom_query=prom_query)
    for prom_data in prom_datas:
        roles = ''
        cmdb_servers_info.insert_record(record_data=prom_data)
        miner_name = prom_data['product'].split('-')[0]
        roles = '-'.join(prom_data['product'].split('-')[1:])
        cmdb_server_miner = prom_data

        cmdb_server_miner['sshport_internal'] = 62534
        cmdb_server_miner['miner_name'] = miner_name
        cmdb_server_miner['roles'] = roles
        cmdb_servers_miner.insert_record(record_data=cmdb_server_miner)

