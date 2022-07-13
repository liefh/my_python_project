# import  subprocess,paramiko,xlwt,xlrd
import paramiko, xlsxwriter

# ip_list = ['172.26.12.112','172.26.12.113']
ip_list = ['10.108.1.133',
'10.108.1.122',
'10.108.1.121',
'10.108.1.127',
'10.108.1.128',
'10.108.1.123',
'10.108.1.125',
'10.108.1.126',
'10.108.1.130',
'10.108.1.132',
'10.108.1.131',
'10.108.1.134',
'10.108.1.138',
'10.108.1.124',
'10.108.1.137',
'10.108.1.139',
'10.108.1.136',
'10.108.1.141',
'10.108.1.142',
'10.108.1.135',
'10.108.1.143']

port = 62534

shell_cpu = "lscpu | grep 'Model name:' | awk  -F ':' '{print $NF}'"
shell_mem = "free -lh |grep 'Mem:' | awk '{print $2}'"
shell_gpu = "nvidia-smi -L"
shell_disk = "parted -l |grep 'Disk /dev/' | grep -v '/dev/md' | awk '{print $2,$3}'"


pkey = '/root/.ssh/id_rsa'
key = paramiko.RSAKey.from_private_key_file(pkey)

workbook = xlsxwriter.Workbook('yh服务器.xlsx')
worksheet = workbook.add_worksheet('yh')
worksheet.write(0, 0, "IP")
worksheet.write(0, 1, "CPU")
worksheet.write(0, 2, "MeM")
worksheet.write(0, 3, "DISK")
worksheet.write(0, 4, "GPU")

row_num = 1
for ip in ip_list:
    print(ip)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(hostname=ip, port=port, username='root', pkey=key, timeout=3, auth_timeout=3)
    stdin, stdout, stderr = ssh.exec_command(shell_cpu)
    result_cpu = stdout.readlines()[0].strip()

    stdin, stdout, stderr = ssh.exec_command(shell_mem)
    result_mem = stdout.readlines()[0].strip()


    stdin, stdout, stderr = ssh.exec_command(shell_disk)
    result_disk=''
    for disk_content in stdout.readlines():
        result_disk = result_disk + disk_content.strip().strip('\n') + ';'

    stdin, stdout, stderr = ssh.exec_command(shell_gpu)
    result_gpu = ''
    for gpu_content in stdout.readlines():
        result_gpu = result_gpu + gpu_content.strip().strip('\n') + ';'

    worksheet.write(row_num, 0, ip)
    worksheet.write(row_num, 1, result_cpu)
    worksheet.write(row_num, 2, result_mem)
    worksheet.write(row_num, 3, result_disk)
    worksheet.write(row_num, 4, result_gpu)


    print(row_num, ip, result_cpu, result_mem, result_disk,result_gpu)
    ssh.close()
    row_num += 1

workbook.close()
print('finished')
