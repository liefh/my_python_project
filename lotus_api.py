import  requests
import json

lotus_url = 'http://47.115.22.33:1234/rpc/v0'
miner_id = "f03367"
# miner_id = "f01019869"
deadline_index=0
# deadline_index=13

headers = {
    'Content-Type' : 'application/json'
}

data = '{"method": "Filecoin.StateMinerPartitions","params":["%s",%s,null], "id": 0}' %(miner_id,deadline_index)

req = requests.post(url=lotus_url,headers=headers,data=data)

ddl_list = json.loads(req.text)['result']


for partition in ddl_list:
    live_sector_bit = partition['LiveSectors']
    print(live_sector_bit)





# curl http://127.0.0.1:1234/rpc/v0 -X POST -H "Content-Type: application/json" -d '{"method": "Filecoin.StateMinerPartitions","params":["f03367",1,null], "id": 0}'
# curl http://127.0.0.1:1234/rpc/v0 -X POST -H "Content-Type: application/json" -d '{"method": "Filecoin.StateMinerPartitions","params":["f01019869",1,null], "id": 14}'