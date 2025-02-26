import re
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 定义文件路径
file_path = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/dump_burst/evaluation-dcqcn.out"

# 定义一个列表存储 CNP 时间
cnp_times = []

# 正则表达式匹配 CNP receive time 数据
pattern = re.compile(r"Node ID: 2, CNP receive time: (\d+) ns")
with open(file_path, "r") as file:
    for line in file:
        match = pattern.search(line)
        if match:
            cnp_times.append(int(match.group(1)))  # 提取时间数据（单位：纳秒）

# 将纳秒转换为秒（如果需要保留纳秒，可省略此步骤）
cnp_times = [time / 1_000_000_000 for time in cnp_times]

# 转换为 Pandas Series
data = pd.Series(cnp_times, name="cnp_time")

# 查看数据
print(data.head())