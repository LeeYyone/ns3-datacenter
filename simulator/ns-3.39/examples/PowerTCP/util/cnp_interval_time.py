import re
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
# 文件路径
file_path = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/dump_burst/evaluation-dcqcn.out"

# 用于存储接收时间
receive_times = []

# 正则表达式匹配 CNP 接收时间
receive_time_pattern = r"Node ID: 3, CNP receive time: (\d+) ns"

# 读取文件并提取接收时间
with open(file_path, "r") as file:
    for line in file:
        match = re.search(receive_time_pattern, line)
        if match:
            # 提取接收时间并存储为整数
            receive_times.append(int(match.group(1)))
# 检查是否有足够的数据：分析频率
# 自定义区间长度（例如 100000 ns = 0.1 ms）
# 转换为 DataFrame
df = pd.DataFrame({"Time (ns)": receive_times})
interval_length = 10000000  # 可调整区间大小
# 找到最小和最大的时间点
min_time = df["Time (ns)"].min()
max_time = df["Time (ns)"].max()

# 生成区间范围
bins = np.arange(min_time, max_time + interval_length, interval_length)

# 将时间点分配到区间
df["Interval"] = pd.cut(df["Time (ns)"], bins=bins, right=False, labels=range(len(bins) - 1))

# 统计每个区间的 CNP 数量
interval_counts = df.groupby("Interval")["Time (ns)"].count()

# 转换为可视化的 DataFrame
interval_df = pd.DataFrame({
    "Interval Index": interval_counts.index,
    "CNP Count": interval_counts.values,
    "Start Time (ns)": bins[:-1],
    "End Time (ns)": bins[1:]
})
print(interval_df)
# 绘制区间内 CNP 数量的柱状图
plt.figure(figsize=(12, 6))
plt.bar(interval_df["Interval Index"], interval_df["CNP Count"], width=0.8, color='skyblue', edgecolor='black')
plt.title("CNP Count per Interval")
plt.xlabel("Interval Index")
plt.ylabel("CNP Count")
plt.grid(axis='y')
plt.show()
result = adfuller(interval_df["CNP Count"])  # intervals 是你的时间间隔列表
print("ADF Statistic:", result[0])
print("p-value:", result[1])
print("Critical Values:", result[4])
if result[1] <= 0.05:
    print("Data is stationary.")
else:
    print("Data is not stationary.")
plot_acf(interval_df["CNP Count"], lags=50)
plot_pacf(interval_df["CNP Count"], lags=20)
plt.show()

start = 0  # 数据起始索引
end = 75   # 数据结束索引
training_data = interval_df["CNP Count"][start:end]

# 构建 ARMA 模型
model = ARIMA(training_data, order=(30, 0, 2))  # p 和 q 通过 ACF 和 PACF 图选择
fitted_model = model.fit()
# 预测未来 10 个点
forecast_steps = 20
forecast = fitted_model.forecast(steps=forecast_steps)
# 绘制实际值与预测值
plt.figure(figsize=(12, 6))
#plt.plot(range(len(interval_df["CNP Count"])), interval_df["CNP Count"], label="Actual Data", marker='o')
forecast_index = range(end, end + forecast_steps)
plt.bar(range(len(interval_df["CNP Count"])), interval_df["CNP Count"], width=0.8, color='skyblue', edgecolor='black')
forecast_index = range(end, end + forecast_steps)
#plt.plot(forecast_index, forecast, label="Forecasted Data", marker='x', linestyle='--')
plt.bar(forecast_index, forecast, width=0.8, color='skyblue', edgecolor='black')

plt.title("ARMA Model: Actual vs Forecasted Intervals")
plt.xlabel("Index")
plt.ylabel("Time Interval (ns)")
plt.legend()
plt.grid()
plt.show()


