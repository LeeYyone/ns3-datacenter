import re

# 文件路径
file_path = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/dump_burst/evaluation-dcqcn.out"

# 用于存储提取的数据
send_times = []
receive_times = []

# 正则表达式匹配 CNP send time 和 CNP receive time
send_time_pattern = r"CNP send time: (\d+) ns"
receive_time_pattern = r"CNP receive time: (\d+) ns"

# 读取文件并提取数据
with open(file_path, "r") as file:
    for line in file:
        send_match = re.search(send_time_pattern, line)
        receive_match = re.search(receive_time_pattern, line)
        if send_match:
            send_times.append(int(send_match.group(1)))  # 提取并存储发送时间
        if receive_match:
            receive_times.append(int(receive_match.group(1)))  # 提取并存储接收时间

# 检查提取的数量是否一致
if len(send_times) != len(receive_times):
    print("WARNING: The number of send times and receive times does not match!")
else:
    print(f"Extracted {len(send_times)} send-receive pairs.")

# 计算 CNP 回传时间
latencies = [receive - send for send, receive in zip(send_times, receive_times)]

# 输出结果
print("CNP Latency Results (ns):")
for i, latency in enumerate(latencies):
    print(f"Pair {i + 1}: Latency = {latency} ns")

# 可选：保存结果到文件
output_file = "../cnp_latency_results_1.txt"
with open(output_file, "w") as file:
    file.write("CNP Latency Results (ns):\n")
    for i, latency in enumerate(latencies):
        file.write(f"Pair {i + 1}: Latency = {latency} ns\n")

print(f"Latency results saved to {output_file}")

