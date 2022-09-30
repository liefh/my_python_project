import  subprocess

cmd = """ls -l /sys/block/ | grep sd | grep -v "$(df -l --output=source / |grep -v Filesystem | sed 's#/dev/##' |sed 's/[0-9]//')" | awk -F'/' '{print $7,$11}' | sed 's/host//' | sort -nk1"""
cmd_return = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf8').stdout.strip()

disk_index = int(cmd_return.split()[0])

result_tmp = ''
for i in cmd_return.strip().split('\n'):
    count = 1
    k = int(i.strip().split()[0])-disk_index
    v = i.strip().split()[1]
    result_tmp = result_tmp + f'{k}--{v} '

print(result_tmp,'\n')

result =f"{result_tmp.strip().split()[0]} {result_tmp.strip().split()[6]} {result_tmp.strip().split()[12]} {result_tmp.strip().split()[18]}\n{result_tmp.strip().split()[1]} {result_tmp.strip().split()[7]} {result_tmp.strip().split()[13]} {result_tmp.strip().split()[19]}\n{result_tmp.strip().split()[2]} {result_tmp.strip().split()[8]} {result_tmp.strip().split()[14]} {result_tmp.strip().split()[20]}\n{result_tmp.strip().split()[3]} {result_tmp.strip().split()[9]} {result_tmp.strip().split()[15]} {result_tmp.strip().split()[21]}\n{result_tmp.strip().split()[4]} {result_tmp.strip().split()[10]} {result_tmp.strip().split()[16]} {result_tmp.strip().split()[22]}\n{result_tmp.strip().split()[5]} {result_tmp.strip().split()[11]} {result_tmp.strip().split()[17]} {result_tmp.strip().split()[23]}"
print(result)
