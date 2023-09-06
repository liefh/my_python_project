#!/usr/bin/env python3

import datetime
import json
import logging
import os
import subprocess
import time
import traceback

import prometheus_client

# handler = handlers.RotatingFileHandler("all.log", mode="a", maxBytes=1024 * 1024 * 10, backupCount=5, encoding="utf-8")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filemode='a')
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# logger.addHandler(handler)

cycles_balance = prometheus_client.Gauge("dfinity_cycles_balance", "Balance of Cycles of Dfinity",
                                         ["name", "canister_id", "project_name"])

cycles_balance_insufficient = prometheus_client.Gauge("cycles_balance_insufficient", "",
                                                      ["name", "canister_id", "project_name"])

icp_balance = prometheus_client.Gauge("dfinity_icp_balance", "Balance of ICP of Dfinity",
                                      ["account_name"])

logger = logging.getLogger("cycles_exporter")
# logger.addHandler(handler)
ENV = os.getenv("ENV")

network = "ic"
project_path = "/Users/mmt/local/dfinity_project"
if ENV == "PRO":
    project_path = "/home/ops/local/WICP"

last_index_map = {
    "yaedc-iqaaa-aaaah-qcnuq-cai": 2,
    "hijcc-dqaaa-aaaah-qcp6q-cai": 3
}

all_discover_canister_info_list = []

exclude_canister_id_list = [
    "jwwek-cqaaa-aaaah-qcrza-cai"
]


class Dfinity:
    decimals = 8
    decimals_dividend = 1e8

    def __init__(self, network, project_path):
        self.network = network
        self.project_path = project_path
        self.transaction_fee = 10000

    def run_cmd(self, cmd, timeout):
        cmd = f"cd {self.project_path};{cmd}"
        logger.info(f"run cmd: {cmd}")

        # if ENV == "LOCAL":
        #     if random.random() > 0.8:
        #         raise Exception("")
        #     return '(opt principal "jwaqi-eqaaa-aaaah-qco4q-cai")\n'

        start_time = datetime.datetime.now()
        try:
            cp = subprocess.run(cmd, shell=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError(f"timeout ({timeout}s)")
        end_time = datetime.datetime.now()
        time_cost = (end_time - start_time).total_seconds()
        logger.info(
            f"cmd run completed  time_cost: {time_cost} cmd: {cmd} returncode: {cp.returncode} stdout: {cp.stdout}, stderr: {cp.stderr}")
        if cp.returncode != 0:
            err_msg = f"run cmd: {cmd} failed, stdout: {cp.stdout} stderr: {cp.stderr}"
            raise Exception(err_msg)
        return cp.stdout


dfinity = Dfinity("ic", project_path)


def discover_canister_ids_item(canister):
    index = 0
    canister_id = canister["id"]
    if canister_id in last_index_map.keys():
        index = last_index_map[canister_id]

    logger.info(f"Discovery from {index} canister_id: {canister_id}")

    canister_info_list = []
    while 1:
        cmd = f"dfx canister --network ic call {canister['id']} getNFTByIndex '({index}:nat)'"
        try:
            stdout = dfinity.run_cmd(cmd, timeout=60)
            canister_id = stdout.split('(opt principal "')[1].split('")')[0]
            canister_info = {
                "name": canister["prefix"] + str(index),
                "project_name": "ccc",
                "method_name": "getCycles",
                "canister_id": canister_id,
                "threshold": canister["threshold"]
            }
            canister_info_list.append(canister_info)
            last_index_map[canister['id']] = index
        except Exception as exc:
            logger.error(f"Discovery from {index} canister_id: {canister_id} error exc: {exc}")
            return canister_info_list
        index += 1


def discover_new_canister_info_list():
    canister_list = [
        {
            "name": "aloneNFT",
            "id": "ouavu-liaaa-aaaah-qbz3a-cai",
            "prefix": "A-",
            "threshold": 0.7
        },
        {
            "name": "multiNFT1155",
            "id": "yaedc-iqaaa-aaaah-qcnuq-cai",
            "prefix": "M-",
            "threshold": 1.5
        },
        {
            "name": "themeNFT1155",
            "id": "hijcc-dqaaa-aaaah-qcp6q-cai",
            "prefix": "T-",
            "threshold": 1.5
        }
    ]

    all_canister_info_list = []

    for canister in canister_list:
        canister_info_list = discover_canister_ids_item(canister)
        all_canister_info_list.extend(canister_info_list)
    return all_canister_info_list

    # cmd = "dfx canister --network ic call otbta-gqaaa-aaaah-qbz3q-cai getAllMultipCanvas"
    #
    # stdout = dfinity.run_cmd(cmd, timeout=60)
    # record_list = []
    # for item in stdout.split("record {")[1:]:
    #     record = {}
    #     record["name"] = "multi_nft_" + str(item.split(" nat; principal")[0].split(" ")[1])
    #     record["canister_id"] = item.split(': nat; principal "')[1].split('"')[0]
    #     record["method_name"] = "getCycles"
    #     record_list.append(record)
    # return record_list


# def get_new_discover_canister_info_list():
#     canister_info_list = discover_new_canister_info_list()
#


def update_cycle_balance(all_discover_canister_info_list):
    with open("canister_ids.json") as f:
        content = f.read()
    canister_info_list = json.loads(content)
    # discover_canister_info_list = discover_canister_info_list()
    # all_discover_canister_info_list += discover_canister_info_list
    canister_info_list = canister_info_list + all_discover_canister_info_list

    for item in canister_info_list:
        name = item["name"]
        canister_id = item["canister_id"]
        project_name = item["project_name"]

        if canister_id in exclude_canister_id_list:
            continue

        try:
            cmd = f"dfx canister --network ic call {canister_id} {item['method_name']}"
            stdout = dfinity.run_cmd(cmd, timeout=60)
            value = stdout.split("(")[1].split(' : nat')[0]
            value = value.replace("_", "")
            value = int(value)
            cycles_balance.labels(name, canister_id, project_name).set(value)
            insufficient = 1
            if value > item["threshold"] * 1e12:
                insufficient = 0
            cycles_balance_insufficient.labels(name, canister_id, project_name).set(insufficient)
        except Exception as exc:
            cycles_balance.labels(name, canister_id, project_name).set(-1)
            cycles_balance_insufficient.labels(name, canister_id, project_name).set(1)
            print(exc)


def update_icp_balance():
    cmd = "dfx identity list"
    stdout = dfinity.run_cmd(cmd, timeout=10)
    account_name_list = stdout.split("\n")
    withdraw_account_name_list = [item for item in account_name_list if item.startswith("withdraw_")]

    for withdraw_account_name in withdraw_account_name_list:
        try:
            cmd = f"dfx --identity {withdraw_account_name} ledger --network ic balance"
            stdout = dfinity.run_cmd(cmd, timeout=60)
            value = stdout.split(" ICP")[0]
            value = float(value)
            icp_balance.labels(withdraw_account_name).set(value)
        except Exception as exc:
            print(exc)


def discover_create_factory_canisters():
    logger.info(f"starting discover_create_factory")

    canister_info_list = []
    cmd = f"dfx canister --network ic call hjiky-uyaaa-aaaah-qc3ka-cai getAllCollInfo"
    try:
        stdout = dfinity.run_cmd(cmd, timeout=60)
        for item in stdout.split('record {\n      "')[1:]:
            # canister_id = stdout.split('(record {"')[1].split('")')[0]
            name = item.split('1_224_700_491 = "')[1].split('";')[0]
            name = name.replace(" ", "")
            canister_id = item.split('4_946_686 = principal "')[1].split('"')[0]
            canister_info = {
                "name": "creator_" + name,
                "project_name": "ccc",
                "method_name": "getCycles",
                "canister_id": canister_id,
                "threshold": 2
            }
            canister_info_list.append(canister_info)
    except Exception as exc:
        logger.error(f"discover_create_factory error exc: {exc}")
    return canister_info_list


if __name__ == '__main__':
    prometheus_client.start_http_server(9113)
    logger.info("started")
    while True:
        try:
            update_icp_balance()
        except Exception as exc:
            logger.warning(traceback.format_exc())

        try:
            update_cycle_balance(all_discover_canister_info_list)
        except Exception as exc:
            logger.warning(traceback.format_exc())

        last_index_map_str = json.dumps(last_index_map)
        logger.info("last_index_map_str: " + last_index_map_str)

        try:
            creator_canister_info_list = discover_create_factory_canisters()
            new_canister_info_list = discover_new_canister_info_list()
            new_canister_info_list_str = json.dumps(new_canister_info_list)
            all_discover_canister_info_list += new_canister_info_list

            all_canister_id_list = [item["canister_id"] for item in all_discover_canister_info_list]
            for item in creator_canister_info_list:
                if item["canister_id"] not in all_canister_id_list:
                    all_discover_canister_info_list.append(item)
                    logger.info(f"add creator canister: {item}")

            logger.info("new_canister_info_list: %s", new_canister_info_list_str)
        except Exception as exc:
            logger.warning(traceback.format_exc())
        logger.info("Round end")
        if ENV == "LOCAL":
            continue
        time.sleep(60 * 1)
