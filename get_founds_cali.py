import requests, json, time

url = 'http://159.65.195.225:12345/testnet3/latest/block'
headers = {
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

try:
    while True:
        response = requests.get(url=url, headers=headers, timeout=(10, 5))
        if response.status_code != 200:
            time.sleep(3)
            continue
        response_dict = json.loads(response.content)
        if 'coinbase' not in response_dict:
            time.sleep(3)
            continue
        break
    date_list = response_dict['coinbase']['partial_solutions']
    count = 0
    for validator in date_list:
        if validator['address'] == 'aleo12lanue3gc76l7sapyswtu6y3uj5rr26myjkdzxc4jdks83wrksys8ypqks':
            count = count + 1
    print(
        f'{time.strftime("%Y-%m-%dT%H:%M:%S")} 一共 : {len(date_list)} | 我们 : {count} | 占比 : {count / len(date_list) * 100}%')
except requests.exceptions as e:
    print(e)
