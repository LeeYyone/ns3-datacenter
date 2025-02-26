import re
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from pmdarima import auto_arima
# 文件路径
file_path = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/util/cnp/cnp_receive_intervals.txt"

# 用于存储时间间隔数据
intervals = []

# 正则表达式匹配时间间隔
interval_pattern = r"Interval \d+: (\d+) ns"

# 读取文件并提取数据（指定读取前多少行）
max_lines = 1000  # 修改为你希望读取的行数
with open(file_path, "r") as file:
    for i, line in enumerate(file):
        if i >= max_lines:  # 如果达到指定的行数则停止读取
            break
        match = re.search(interval_pattern, line)
        if match:
            intervals.append(int(match.group(1)))  # 提取时间间隔数据

# 检查提取结果
if len(intervals) == 0:
    raise ValueError("No time intervals found in the file.")
else:
    print(f"Extracted {len(intervals)} intervals.")

# 将数据构建为 pandas DataFrame
df = pd.DataFrame(intervals, columns=["Interval (ns)"])

# 自动选择 ARIMA 参数
model = auto_arima(df["Interval (ns)"], seasonal=False, trace=True, stepwise=True)
print(model.summary())
# 打印模型摘要
print(model.summary())

# 预测未来 10 个点
forecast_steps = 100
forecast = model.predict(n_periods=forecast_steps)

# 可视化实际值与预测值
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Interval (ns)"], label="Original Data", marker='o')
forecast_index = range(len(df), len(df) + forecast_steps)
plt.plot(forecast_index, forecast, label="Forecasted Data", marker='x', linestyle='--')
plt.title("ARIMA Model: Original Data and Forecast")
plt.xlabel("Index")
plt.ylabel("Interval (ns)")
plt.ylim(0,10000000)
plt.legend()
plt.grid()
plt.show()
