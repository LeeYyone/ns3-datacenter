import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
def extract_latencies(file_path):
    """从文件中提取延迟数据"""
    latencies = []
    with open(file_path, "r") as file:
        for line in file:
            if "Latency =" in line:
                # 提取延迟值
                latency = int(line.split("Latency =")[1].strip().replace(" ns", ""))
                latencies.append(latency)
    return latencies
# 将 CDF 数据保存到同一个 sheet 的不同列
def save_cdf_to_single_sheet(latencies1, cdf1, latencies2, cdf2, output_file):
    """保存两个文件的 CDF 数据到一个 sheet 的不同列"""
    # 找到最长数组的长度
    max_len = max(len(latencies1), len(latencies2))

    # 转换为浮点数类型，并使用 NaN 填充数组，使长度一致
    latencies1 = np.array(latencies1, dtype=float)
    cdf1 = np.array(cdf1, dtype=float)
    latencies2 = np.array(latencies2, dtype=float)
    cdf2 = np.array(cdf2, dtype=float)

    latencies1 = np.pad(latencies1, (0, max_len - len(latencies1)), constant_values=np.nan)
    cdf1 = np.pad(cdf1, (0, max_len - len(cdf1)), constant_values=np.nan)
    latencies2 = np.pad(latencies2, (0, max_len - len(latencies2)), constant_values=np.nan)
    cdf2 = np.pad(cdf2, (0, max_len - len(cdf2)), constant_values=np.nan)

    # 创建 DataFrame
    df = pd.DataFrame({
        "Latency File1 (ns)": latencies1,
        "CDF File1": cdf1,
        "Latency File2 (ns)": latencies2,
        "CDF File2": cdf2
    })
    df.to_excel(output_file, index=False, sheet_name="CDF Comparison")
file1 = "../cnp_latency_results.txt"
file2 = "../cnp_latency_results_1.txt"
# 处理后的数据文件路径
output_excel_file = "cnp/processed_latencies.xlsx"
# 提取数据
latencies1 = extract_latencies(file1)
latencies2 = extract_latencies(file2)

# 生成 CDF 数据
sorted_latencies1 = np.sort(latencies1)
cdf1 = np.arange(1, len(sorted_latencies1) + 1) / len(sorted_latencies1)

sorted_latencies2 = np.sort(latencies2)
cdf2 = np.arange(1, len(sorted_latencies2) + 1) / len(sorted_latencies2)

# 绘制 CDF 图表
plt.figure(figsize=(8, 6))
plt.plot(sorted_latencies1, cdf1, marker="o", linestyle="-", label="File 1 CNP Latency CDF", markersize=1)
plt.plot(sorted_latencies2, cdf2, marker="s", linestyle="--", label="File 2 CNP Latency CDF", markersize=1)
plt.xlabel("Latency (ns)")
plt.ylabel("CDF")
plt.title("CNP Latency CDF Comparison")
plt.grid(True)
plt.legend()
plt.show()
# 保存两个文件的 CDF 数据到不同的 sheet
if os.path.exists(output_excel_file):
    os.remove(output_excel_file)  # 如果文件已存在，先删除它
# 保存 CDF 数据
save_cdf_to_single_sheet(sorted_latencies1, cdf1, sorted_latencies2, cdf2, output_excel_file)

print(f"Processed data saved to {output_excel_file}.")