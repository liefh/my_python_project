import requests

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Content-Type':'application/json'
}

aleo_url = 'https://backend.faucet.aleo.org/testnet3/faucet/getFaucetRequests'

response = requests.get(url=aleo_url,headers=headers).json()['processed_texts']


owner_address = 'aleo1guz0hjjwsn48s9yahhet0n0he4g4dfv32955v0ypv7lsdz2k9spss5xv88'
owner_address_amount = 0

for address in response:
    # if address['address'] == 'aleo1cqkykw3jr43tjdu4t2w25cj5w96gcmk3qukvet8hdme3vtsqw5gs25ff4q':
    if address['address'] == owner_address:
        owner_address_amount += address['amount']



print(f"{owner_address} 累计积分: {owner_address_amount/10000}w")