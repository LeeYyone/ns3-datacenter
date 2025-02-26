import re
import matplotlib.pyplot as plt

# 定义文件路径
file_path = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/dump_burst/evaluation-dcqcn.out"

# 定义一个列表用于存储时间数据
cnp_times = []

pattern = re.compile(r"Node ID: 2, CNP receive time: (\d+) ns")

# 读取文件并提取时间数据
with open(file_path, "r") as file:
    for line in file:
        match = pattern.search(line)
        if match:
            cnp_times.append(int(match.group(1)))

# 将时间数据转换为秒
cnp_times = [time / 1000000000 for time in cnp_times]

# 打印数据范围
print("Minimum CNP time (s):", min(cnp_times))
print("Maximum CNP time (s):", max(cnp_times))

# 绘制分布图
plt.figure(figsize=(10, 6))
plt.hist(cnp_times, bins=100000, alpha=0.7, edgecolor="black")
plt.title("CNP Receive Time Distribution")
plt.xlabel("CNP Receive Time (s)")
plt.ylabel("Frequency")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.xlim(1.04, 1.12)
plt.show()