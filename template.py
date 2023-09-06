import logging
import subprocess


subprocess.run()


logging.basicConfig(
    # filename='xxx',
    # filemode='a',
    # encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s %(filename)s %(funcName)s[line:%(lineno)d]',
    datefmt="%FT%T",
)


def exec_cmd(cmd):
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True,encoding='utf-8')
        stdout, stderr = process.communicate()
        stdout, stderr = stdout.strip(), stderr.strip()
        if len(stderr) != 0:
            return stderr
        return stdout
    except Exception as err:
        print(err)