gpu_num = 8
cpu_core = 128
cpu_core_start = 0
core_offset = int(cpu_core / gpu_num)
job_num = 40
bench_cmd = '/root/bench-intel-v6.0.0'
log_dir = '/root/'

for i in range(0, gpu_num):
    cpu_core_end = cpu_core_start + core_offset
    print(
        # f"FORCE_GPU_MINER=1 RUST_LOG=trace FORCE_BATCH_MSM=1 CUDA_VISIBLE_DEVICES={i} CORE_OFFSET={cpu_core_start} CORE={core_offset}  N={job_num} taskset -c {cpu_core_start}-{cpu_core_end - 1} {bench_cmd} &> {log_dir}gpu{i}-core{core_offset}.log &")
        f"mkdir -p /sys/fs/cgroup/cpuset/bench-gpu{i} && echo {cpu_core_start}-{cpu_core_end} > /sys/fs/cgroup/cpuset/bench-gpu{i}/cpuset.cpus;FORCE_GPU_MINER=1 RUST_LOG=trace FORCE_BATCH_MSM=1 CUDA_VISIBLE_DEVICES={i} CORE_OFFSET={cpu_core_start} CORE={core_offset}  N={job_num} taskset -c {cpu_core_start}-{cpu_core_end - 1} {bench_cmd}-{i} &> {log_dir}gpu{i}-core{core_offset}.log &  echo $(ps -ef | grep bench-intel-v6.0.0-{i} | grep -v grep | awk 'print $2') > /sys/fs/cgroup/cpuset/bench-gpu{i}/cgroup.procs")
    cpu_core_start = cpu_core_end