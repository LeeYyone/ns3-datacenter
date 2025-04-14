import pandas as pd
import matplotlib.pyplot as plt

# 读取实验结果的 Excel 文件
file_path = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/experiment_results3.xlsx"  # 请确保更新为你的文件路径
data = pd.read_excel(file_path)

# 计算 FCT (ns) Flow 1 相比 Standalone FCT (ns) Flow 1 增长的倍数
data['FCT_Flow1_vs_Standalone_FCT_Flow1'] = data[' FCT (ns) Flow 1'] / data[' Standalone FCT (ns) Flow 1']
data['FCT_Flow2_vs_Standalone_FCT_Flow2'] = data[' FCT (ns) Flow 2'] / data[' Standalone FCT (ns) Flow 2']

# 绘制图形
plt.figure(figsize=(20, 6))
plt.plot(data['Flow Size (Bytes)'], data['FCT_Flow1_vs_Standalone_FCT_Flow1'], marker='o', linestyle='-', color='b' , markersize=10)
# plt.plot(data['Flow Size (Bytes)'], data['FCT_Flow2_vs_Standalone_FCT_Flow2'], marker='o', linestyle='-', color='r' , markersize=1)

# 添加标题和标签
plt.title('FCT Flow 1 vs Standalone FCT Flow 1 Growth Factor vs Flow Size')
plt.xlabel('Flow Size (Bytes)')
plt.ylabel('FCT (ns) Flow 1 / Standalone FCT (ns) Flow 1')

# 显示图形
plt.grid(True)
plt.show()
