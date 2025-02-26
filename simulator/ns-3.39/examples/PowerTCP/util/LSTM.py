import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# 文件路径
file_path = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/util/cnp/cnp_receive_intervals.txt"

# 数据提取
intervals = []
interval_pattern = r"Interval \d+: (\d+) ns"
with open(file_path, "r") as file:
    for line in file:
        match = re.search(interval_pattern, line)
        if match:
            intervals.append(int(match.group(1)))

# 检查提取结果
if len(intervals) == 0:
    raise ValueError("No time intervals found in the file.")
df = pd.DataFrame(intervals, columns=["Interval (ns)"])

# 数据归一化
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df["Interval (ns)"].values.reshape(-1, 1))

# 准备训练数据
lookback = 10  # 过去 10 个点预测下一个点
X, y = [], []
for i in range(lookback, len(scaled_data)):
    X.append(scaled_data[i-lookback:i, 0])
    y.append(scaled_data[i, 0])
X, y = np.array(X), np.array(y)

# 数据分割为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 重塑数据为 LSTM 输入格式
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# 构建 LSTM 模型
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(optimizer="adam", loss="mean_squared_error")

# 训练模型
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=20, batch_size=32)

# 绘制训练和验证损失
plt.figure(figsize=(12, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('LSTM Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid()
plt.show()

# 预测未来 10 个点
predicted = []
current_input = scaled_data[-lookback:].reshape(1, lookback, 1)
for _ in range(10):
    next_value = model.predict(current_input)[0, 0]
    predicted.append(next_value)
    current_input = np.append(current_input[:, 1:, :], [[next_value]], axis=1)

# 反归一化预测结果
predicted = scaler.inverse_transform(np.array(predicted).reshape(-1, 1))

# 绘制实际值与预测值
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Interval (ns)"], label="Original Data", marker='o')
forecast_index = range(len(df), len(df) + len(predicted))
plt.plot(forecast_index, predicted, label="LSTM Forecast", marker='x', linestyle='--')
plt.title("LSTM Model: Original Data and Forecast")
plt.xlabel("Index")
plt.ylabel("Interval (ns)")
plt.legend()
plt.grid()
plt.show()
