import argparse
import time
import subprocess
import os
import toml


file_name = __file__

miners_id_name = {'hk01': 'f01228105',
                  'hk02': 'f01228100',
                  'hk03': 'f01228087',
                  'hk04': 'f01228089',
                  'hk10': 'f01984576',
                  'hk11': 'f01984586',
                  'hk12': 'f01984593'
                  }

this_date = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))

# 只能传参 hk01,hk02,hk03,hk04,hk10,hk11,hk12旷工号
parser = argparse.ArgumentParser(description=f'只能传参 hk01,hk02,hk03,hk04,hk10,hk11,hk12 旷工号中的一个，比如 : {__file__} hk01')
parser.add_argument('-n', '--miner_name', type=str,required=True, default=None,choices=['hk01','hk02','hk03','hk04','hk10','hk11','hk12'], help='hk01,hk02,hk03,hk04,hk10,hk11,hk12 旷工号中的一个')
args = parser.parse_args()


if args.miner_name is None:
    parser.print_help()
    exit(3)


def exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.poll() != 0:
            return stderr.decode()
        return process.returncode
    except Exception as err:
        return err,stderr.decode()


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        # filename='xxx',
        # filemode='a',
        # encoding='utf-8',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt="%FT%T",
    )

    miner_name = args.miner_name
    home_dir='/root'
    work_dir='/root'
    qn_config_dir='/root/change_vsm/qn_config'
    vsm_config_dir='/root/change_vsm/vsm_config'
    mount_point = '/mnt/qn /mnt/qn02 /mnt/qn03 /mnt/qn04 /mnt/qn05'
    process_name = 'venus-sector-manager slaver-wdpost'
    backup_dir='/tmp'

    try:
        # 卸载,备份老配置,停服务
        exec_cmd(f'umount -lf {mount_point}')
        exec_cmd(f'umount -lf {mount_point}')
        exec_cmd(f'mv {work_dir}/.venus-sector-manager {backup_dir}/.venus-sector-manager_bak{this_date}')
        exec_cmd(f'mv {work_dir}/wdpost {backup_dir}/wdpost_bak{this_date}')
        exec_cmd(f'supervisorctl stop {process_name}')
        logging.info(f'{mount_point}已卸载')
        logging.info(f'{work_dir}/.venus-sector-manager已备份到{backup_dir}目录')
        logging.info(f'{work_dir}/wdpost已备份到{backup_dir}目录')
        logging.info(f'{process_name}服务已停止')

        # 挂载
        for qn_mount_dir in os.listdir(f'{qn_config_dir}/{miner_name}'):
            exec_cmd(f'nohup {qn_config_dir}/{miner_name}/{qn_mount_dir}/fcfs.sh -e -s 1> {qn_config_dir}/{miner_name}/{qn_mount_dir}/fcfs.log 2>&1 &')
            exec_cmd(f'{qn_config_dir}/{miner_name}/{qn_mount_dir}/fcfs.sh sync')
            logging.info(f'{qn_mount_dir}已挂载')
        time.sleep(5)


        # 准备新的配置文件
        exec_cmd(f'mkdir {work_dir}/.venus-sector-manager')
        exec_cmd(f'cp -f {vsm_config_dir}/{miner_name}/.venus-sector-manager/sector-manager.cfg {work_dir}/.venus-sector-manager/')
        exec_cmd(f'cp -f {vsm_config_dir}/{miner_name}/.venus-sector-manager/ext-prover.cfg {work_dir}/.venus-sector-manager/')
        exec_cmd(f'cp -rf {vsm_config_dir}/{miner_name}/wdpost {work_dir}/')
        logging.info('新的配置文件已准备')

        # attach
        sector_manager_cfg=toml.load(f'{vsm_config_dir}/{miner_name}/.venus-sector-manager/sector-manager.cfg')
        Common_PersistStores=sector_manager_cfg['Common']['PersistStores']
        for Common_PersistStore in Common_PersistStores:
            Common_PersistStore_name=Common_PersistStore['Name']
            Common_PersistStore_path=Common_PersistStore['Path']
            logging.info(f'正在执行{work_dir}/venus-sector-manager util storage attach --verbose --name={Common_PersistStore_name} {Common_PersistStore_path}，请耐心等待！！')
            exec_cmd(f'{work_dir}/venus-sector-manager util storage attach --verbose --name={Common_PersistStore_name} {Common_PersistStore_path}')
        logging.info('attach已完成')


        # 启动
        exec_cmd(f'supervisorctl start {process_name}')

        # check_health
        logging.info("\033[32m备机已启动，请check！\033[0m")
        check_ddl = r"for i in {0..47};do "+f"{work_dir}/venus-sector-manager util sealer proving --miner {miners_id_name[miner_name]} check $i;done"
        logging.info(check_ddl)



    except Exception as err:
        logging.error("\031[31m备机启动异常\031[0m")
        logging.error(err)