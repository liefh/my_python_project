import subprocess
import sys
import logging
from supervisor import childutils
import time

logging.basicConfig(
    # filename='xxx',
    # filemode='a',
    # encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt="%FT%T",
)

def exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.poll() != 0:
            return stderr.decode()
        return process.returncode
    except Exception as err:
        return err, stderr.decode()


AUTH_CMD='''sudo -u fil expect << EOF
spawn /home/fil/venus-wallet-pro  wallet connect_author --authorizer http://47.111.118.229:9528/rpc/v0
expect "*user:"
send "huihuang\n"
expect "password:"
send "renran\n"
expect eof
EOF'''



if __name__ == '__main__':
    try:
        stdin = sys.stdin
        stdout = sys.stdout
        stderr = sys.stderr
        while True:
            headers, payload = childutils.listener.wait(stdin, stdout)
            if headers['eventname'] == 'PROCESS_STATE_RUNNING':
                time.sleep(10)
                auth_exit_code = exec_cmd(AUTH_CMD)
                if auth_exit_code != 0:
                    logging.error('认证失败，请手动认证')
                    exit(3)
                logging.info('认证成功。')


            # stderr.write(str(headers)+'\n')
            # stderr.flush()

            # stderr.write(str(payload)+'\n')
            # stderr.flush()
            childutils.listener.ok(stderr)
            childutils.listener.ok(stdout)


    except Exception as e:
        logging.error(e)