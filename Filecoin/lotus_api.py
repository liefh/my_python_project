import requests
import json

# Lotus节点的API地址
lotus_api_url = 'https://api.node.glif.io/rpc/v0'


headers = {
    'Content-Type': 'application/json',
}


# method_data = {
#     "jsonrpc": "2.0",
#     "method": "Filecoin.StateMinerPower",
#     "params": ["t0101", None],
#     "id": 3
# }
method_data = {
    "jsonrpc": "2.0",
    "method": "Filecoin.StateMinerActiveSectors",
    "params": [
          "f01234",
          [
            {
              "/": "bafy2bzacea3wsdh6y3a36tb3skempjoxqpuyompjbmfeyf34fi3uy6uue42v4"
            },
            {
              "/": "bafy2bzacebp3shtrn43k7g3unredz7fxn4gj533d3o43tqn2p2ipxxhrvchve"
            }
          ]
       ],
    "id": 7878
}


response = requests.post(url=lotus_api_url,headers=headers,data=json.dumps(method_data))

print(response.json())