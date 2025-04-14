#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

# —— 1. PCIe5.0 带宽常量 —— #
LANE_RATE_GTPS    = 32e9            # 32 GT/s per lane (bits/s)
ENCODING_OVERHEAD = 128 / 130        # 128b/130b 编码效率
LANES             = 16              # x16
PCIE5_BW_BPS      = LANE_RATE_GTPS * ENCODING_OVERHEAD * LANES   # bits/s
PCIE5_BW_BYTES    = PCIE5_BW_BPS / 8                             # bytes/s

print(f"Assumed PCIe5.0 bandwidth: {PCIE5_BW_BYTES/1e9:.2f} GB/s\n")

# —— 2. 读入 task_flow_relations.txt —— #
# 此处假设文件首行是中文表头（如“任务ID 源节点 ...”）
relations = pd.read_csv(
    '/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/my_file/task_flow_relations.txt',
    sep='\s+',       # 用任意空白符分隔
    header=0,        # 第一行是表头
    dtype={'任务ID': int, '源节点': int, '目标节点': int, '数据大小': float, '开始时间': float}
)

# 重命名列名为英文方便后续处理
relations = relations.rename(columns={
    '任务ID': 'task_id',
    '源节点': 'src',
    '目标节点': 'dst',
    '数据大小': 'size_bytes',
    '开始时间': 'start_time'
})

# 根据 src 与 dst 判定流类型
relations['type'] = relations.apply(lambda r: 'intra' if r.src == r.dst else 'inter', axis=1)
# 生成 fct.txt 中使用的节点ID，这里假设每个节点按格式 "0b000{node}01"
relations['src_id'] = relations['src'].apply(lambda x: f"0b000{x:0>1x}01")
relations['dst_id'] = relations['dst'].apply(lambda x: f"0b000{x:0>1x}01")

# —— 3. 读入 fct.txt —— #
# fct.txt 文件每行格式：src_id  dst_id  sport  dport  size_bytes  <unused>  finish_time  start_time
colnames = ['src_id', 'dst_id', 'sport', 'dport', 'size_bytes_fct', 'start', 'fct', 'fct_theo']
fct = pd.read_csv(
    '/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/dump_burst/fct.txt',
    sep='\s+',
    names=colnames,
    dtype={'src_id': str, 'dst_id': str, 'start': int, 'fct': int, 'fct_theo': int}
)
# 仿真给的是纳秒级时间戳，这里转换成秒
fct['fct_seconds'] = fct['fct'] / 1e9

# —— 4. 合并两份数据 & 计算每个流的完成时间 —— #
df = pd.merge(
    relations,
    fct[['src_id', 'dst_id', 'fct_seconds']],
    on=['src_id', 'dst_id'],
    how='left'
)

def compute_fct(row):
    if row['type'] == 'inter':
        # 跨节点流：直接使用仿真中记录的完成时间
        return row['fct_seconds']
    else:
        # 节点内流：根据 PCIe5.0 带宽计算
        return row['size_bytes'] / PCIE5_BW_BYTES

df['computed_fct'] = df.apply(compute_fct, axis=1)

# 如果有跨节点流没有从 fct.txt 得到完成时间，给出警告
missing = df[(df['type'] == 'inter') & (df['fct_seconds'].isna())]
if not missing.empty:
    print("Warning: 以下跨节点流在 fct.txt 中未找到对应完成时间：")
    print(missing[['src_id', 'dst_id']].to_string(index=False))
print()

# —— 5. 输出详细信息 —— #
print("每个任务的各个流详情如下：\n")
# 以任务ID排序，便于阅读
df_sorted = df.sort_values(by='task_id')

# 按任务分组逐个输出
for task_id, group in df_sorted.groupby('task_id'):
    print(f"任务 {task_id}:")
    # 初始化任务累计完成时间
    task_total_time = 0
    for idx, row in group.iterrows():
        flow_type = row['type']
        src = row['src']
        dst = row['dst']
        size_mb = row['size_bytes'] / (1024 * 1024)
        # 如果跨节点流，则输出 fct_seconds 否则计算出的节点内流时间
        flow_time = row['computed_fct']
        task_total_time += flow_time
        print(f"  流 {idx}: 节点 {src} -> 节点 {dst} | 类型: {flow_type} | 数据大小: {size_mb:.2f} MB | 流完成时间: {flow_time:.6f} 秒")
    print(f"  => 任务 {task_id} 总完成时间: {task_total_time:.6f} 秒\n")

# —— 6. 输出每个任务的总完成时间汇总 —— #
task_times = (
    df
    .groupby('task_id', as_index=False)['computed_fct']
    .sum()
    .rename(columns={'computed_fct': 'task_completion_time_s'})
)

print("各任务完成时间汇总：")
print(task_times.to_string(index=False))
