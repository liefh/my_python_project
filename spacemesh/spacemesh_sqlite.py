import sqlite3
import bech32

sqlite_path =r'C:\Users\Administrator\Desktop\state.sql'

our_address = [
    {'openstack':'sm1qqqqqq97ygsmk5nsa4uy5vztgq2tj5fkpknjrrcxl37cu'},
    {'yz':'sm1qqqqqqzmt7dcrfccd4n3c76q3jfnnx0fj8uuy7q22laey'},
    {'jh':'sm1qqqqqqza0ppemf98djf65jrpdsm3lnw05xtc6kg70vkxl'},
    {'cs':'sm1qqqqqqrsgs5zd059zjeuj5kerzlccc7ursl29dq86sf4j'},
    {'tony_10w':'sm1qqqqqq83wd3qt30gyeqhak0rxdsupj487wz3tvg3ludcf'},
    {'yunxiao_3':'sm1qqqqqqxzz7y8e6a0c3jkc9dmh3m0s3tutav5v7ssru09x'},
    {'yunxiao_4':'sm1qqqqqqrqdpwve42h3hasngqc5qjna4t3520jajqazt4dq'},
    {'hpool':'sm1qqqqqqpzvpdcm0c09aac3fvzywmt7v0dyqvpygq55xla6'},
]

sql = 'select coinbase,COUNT(pubkey) as nodes_num,SUM(effective_num_units) as units_num from atxs WHERE epoch=3  GROUP BY coinbase;'



def node_id_to_address(node_id):
    hrp = 'sm'
    data = bytes.fromhex(node_id)
    converted_data = bech32.convertbits(data, 8, 5)  # 将字节数据从 8 位转换为 5 位
    return bech32.bech32_encode(hrp, converted_data)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect(sqlite_path)
conn.row_factory = dict_factory
cur = conn.cursor()
cur.execute(sql)

res = cur.fetchall() # type:dict
# print(res)
data = []
our_data = []

total_power = 0
total_units = 0
total_nodes = 0
for atx in res:
    atx['coinbase'] = node_id_to_address(atx['coinbase'].hex())
    atx['power'] = atx['units_num']*64/1024
    total_power = total_power + atx['power']
    total_units = total_units + atx['units_num']
    total_nodes = total_nodes + atx['nodes_num']
    data.append(atx)
    if atx['coinbase'] in [address_list for address in our_address for address_list in address.values()]:
        our_data.append(atx)



for i in our_data:
    print(i,'  占比 : ',round(i['power']/total_power*100,2),'%')

print('\n'+'--'*10)
print('total_coinbases :',len(data))
print('total_nodes :',total_nodes)
print('total_units :',total_units)
print('total_power :',total_power,'TiB')