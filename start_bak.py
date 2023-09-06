import argparse
import time
import subprocess

miners_id_name = {
    'f01228105': 'hk01',
    'f01228100': 'hk02',
    'f01228087': 'hk03',
    'f01228089': 'hk04'
}

# lotus_ip = {
#     'hk01': '20.2.1.27',
#     'hk02': '20.2.1.28',
#     'hk03': '20.2.1.29',
#     'hk04': '20.2.1.30'
# }

lotus_servers_ip = {
    'hk01': '47.242.42.180',
    'hk02': '47.242.239.152',
    'hk03': '8.210.93.104',
    'hk04': '8.210.32.230'
}

write_tokens = {
    'hk01': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiaGstMDEtd2FsbGV0IiwicGVybSI6InJlYWQiLCJleHQiOiIifQ.rcNHiyArh_tESZxpWCYqvAQjVNqrmXRZaOR3dtWnIck',
    'hk02': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiaGstMDIiLCJwZXJtIjoid3JpdGUiLCJleHQiOiIifQ.JjjjVYAlpHkHiBASGkzgpM5pWLPOAT3uIzZNO1Pj5gY',
    'hk03': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiaGstMDMiLCJwZXJtIjoid3JpdGUiLCJleHQiOiIifQ.at-4WOFD1Z6MXaRsaVlyEnP1zawT8pLKGU-tCMNzwN4',
    'hk04': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiaGstMDQiLCJwZXJtIjoid3JpdGUiLCJleHQiOiIifQ.L0PpA_5_Rc1dpzmyfK7z1AT6ZLZUjqHfjiL6JiuHuSc'
}

this_date = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))

# 只能传参 hk-01 到 hk-04 旷工号
parser = argparse.ArgumentParser(description='只能传参 hk-01 到 hk-04 旷工号中的一个')
parser.add_argument('-m', '--miner_id', type=str, help='hk-01 到 hk-04 旷工号中的一个')
args = parser.parse_args()

if args.miner_id is None:
    parser.print_help()
    exit(3)

if args.miner_id not in miners_id_name.keys():
    parser.print_help()
    exit(3)

def exec_cmd(cmd):
    result = subprocess.run(cmd,shell=True)
    if result.returncode != 0:
        return result.stderr


try:
    miner_name = miners_id_name.get(args.miner_id)

    # 关停老业务,备份老配置
    exec_cmd('umount -lf /mnt/qn')
    exec_cmd('umount -lf /mnt/qn')
    exec_cmd('supervisorctl stop window-poster winning-poster')

    exec_cmd(f'mv /root/kodo-fcfs/fcfs.conf /tmp/fcfs.conf_bak{this_date}')
    exec_cmd(f'mv /home/fil/qiniu-cfg.toml /tmp/qiniu-cfg.toml_bak{this_date}')
    exec_cmd(f'mv /home/fil/.lotus/token /tmp/.lotus/token_bak{this_date}')
    exec_cmd(f'mv /home/fil/.lotusposter /tmp/.lotusposter_bak{this_date}')

    # 准备配置文件
    exec_cmd(f'cp /home/fil/hk01-02-03-04/fcfs.conf_{miner_name} /root/kodo-fcfs/fcfs.conf')
    exec_cmd(f'cp /home/fil/hk01-02-03-04/qiniu-cfg.toml_{miner_name}  /home/fil/qiniu-cfg.toml')

    exec_cmd(f'cp /home/fil/hk01-02-03-04/token_{miner_name} /home/fil/.lotus/token')
    exec_cmd(f'sudo -u fil /home/fil/lotus-miner poster --mode=windows --server-api=http://{lotus_servers_ip.get(miner_name)}:3456')
    exec_cmd('mv /home/fil/.lotusposter/config.toml /tmp/')
    exec_cmd(f'cp /home/fil/hk01-02-03-04/config.toml_{miner_name} /home/fil/.lotusposter/config.toml')
    exec_cmd(
        f"sed -i '/^command/c command=/home/fil/lotus-miner poster --mode=windows --server-api=http://{lotus_servers_ip.get(miner_name)}:3456' /etc/supervisord.d/winning-poster.ini")
    exec_cmd(
        f'''sed -i '/^scheduler_url/c scheduler_url = "http://{lotus_servers_ip.get(miner_name)}:3456"' /home/fil/config.toml''')

    # 启动
    exec_cmd('/root/kodo-fcfs/fcfs.sh -e -s 1> /root/kodo-fcfs/fcfs.log 2>&1 &')
    exec_cmd('supervisorctl update window-poster winning-poster')
    exec_cmd('supervisorctl start window-poster winning-poster')
except Exception as err:
    print(err)


print("检查 config.toml .lotus/api qiniu-cfg.toml 和进程启动无异常后，执行init 和 add ")
print(f'TRUST_PARAMS=1  ./lotus-miner init --owner={args.miner_id} --sector-size 34359738368 ')
print(f'./lotus-miner poster add --addr={args.miner_id} --prover-type=remote --dist-path=/mnt/qn')