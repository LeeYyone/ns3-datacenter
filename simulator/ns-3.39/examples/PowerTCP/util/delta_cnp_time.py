import re
import matplotlib.pyplot as plt

# 文件路径
file_path = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/dump_burst/evaluation-dcqcn.out"

# 用于存储接收时间
receive_times = []

# 正则表达式匹配 CNP receive time
receive_time_pattern = r"CNP receive time: (\d+) ns"

# 读取文件并提取接收时间
with open(file_path, "r") as file:
    for line in file:
        receive_match = re.search(receive_time_pattern, line)
        if receive_match:
            receive_times.append(int(receive_match.group(1)))  # 提取并存储接收时间

# 检查是否提取到足够的接收时间
if len(receive_times) < 2:
    print("WARNING: Not enough receive times to calculate intervals!")
else:
    print(f"Extracted {len(receive_times)} CNP receive times.")

# 计算接收时间间隔
intervals = [receive_times[i] - receive_times[i - 1] for i in range(1, len(receive_times))]

# 输出时间间隔
print("CNP Receive Time Intervals (ns):")
for i, interval in enumerate(intervals):
    print(f"Interval {i + 1}: {interval} ns")

# 绘制时间间隔折线图
plt.figure(figsize=(12, 6))
plt.plot(range(1, len(intervals) + 1), intervals, marker='o',markersize=1, linestyle='-', label="Time Intervals")
plt.title("CNP Receive Time Intervals")
plt.xlabel("Interval Index")
plt.ylabel("Time Interval (ns)")
plt.ylim(0,10000000)
plt.grid()
plt.legend()
plt.show()

# 可选：保存结果到文件
output_file = "cnp/cnp_receive_intervals.txt"
with open(output_file, "w") as file:
    file.write("CNP Receive Time Intervals (ns):\n")
    for i, interval in enumerate(intervals):
        file.write(f"Interval {i + 1}: {interval} ns\n")

print(f"Receive time intervals saved to {output_file}")
