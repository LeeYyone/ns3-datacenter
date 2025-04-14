import pandas as pd

# 定义文件路径
txt_file = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/experiment_results3.txt"
excel_file = "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/experiment_results4.xlsx"

# 读取 TXT 文件
data = pd.read_csv(txt_file)

# 将数据保存为 Excel 文件
data.to_excel(excel_file, index=False)

print(f"TXT file has been successfully converted to Excel: {excel_file}")
