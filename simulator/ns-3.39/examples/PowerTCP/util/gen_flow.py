import random

# 每个节点有 8 个 GPU
NUM_GPUS = 8
DATA_SIZE = 1024 * 1024 * 1024  # 1GB 数据大小，单位是字节
TRANSFER_SPEED = 25  # 1GB/秒的传输速率

# 定义任务的通信模式：假设每个任务通信模式是环形的，按顺序依次进行通信
def generate_communication_path(task_gpus):
    path = task_gpus + [task_gpus[0]]  # 环形通信路径，最后返回源节点
    return path

# 根据任务部署信息生成流量文件内容
def generate_traffic_file(task_deployments):
    traffic_file_content = []
    
    # 初始化每个任务的起始时间
    task_end_time = {}  # 用来存储每个任务最后一个节点的传输结束时间
    
    # 遍历每个任务的部署信息
    for task_id, task_gpus in task_deployments.items():
        # 生成通信路径
        comm_path = generate_communication_path(task_gpus)
        
        # 初始化任务的起始时间
        start_time = 0.1  # 第一个通信的起始时间设为 0.1 秒
        
        # 遍历通信路径，生成每个流量的配置
        for i in range(len(comm_path) - 1):
            src_node, src_gpu = comm_path[i]
            dst_node, dst_gpu = comm_path[i + 1]
            
            # 如果源节点和目标节点相同，则是节点内GPU通信
            
            # 不跳过节点内通信，而是要标记这些流属于同一任务
            transfer_time = DATA_SIZE / (TRANSFER_SPEED * 1024 * 1024 * 1024)  # 以秒为单位
            
            # 假设每个节点的端口号与节点编号一致，节点1对应端口10001，节点2对应端口10002等
            src_port = 10000 + src_node
            dst_port = 10000 + dst_node
            
            # 添加任务ID，表示这条流属于哪个任务
            traffic_file_content.append((task_id, src_node, dst_node, 3, src_port, DATA_SIZE, start_time))
            
            # 更新下一次通信的起始时间
            start_time += transfer_time
    
    # 按照流的起始时间进行排序
    traffic_file_content.sort(key=lambda x: x[6])  # 根据起始时间进行排序
    
    return traffic_file_content

# 输入：任务部署信息，每个任务部署在多个 GPU 上，形式为 (节点编号, GPU编号)
# 第一种情况的拓扑
task_deployments = {
    1: [(1, 1), (2, 1), (3, 1), (4, 1)],  # 任务1，部署在节点1的GPU1、GPU2和节点2的GPU1、GPU2 
    2: [(5, 1), (2, 2), (2, 3), (2, 4)],  # 任务2，部署在节点1的GPU3、GPU4和节点3的GPU1、GPU2 
    3: [(6, 1), (7, 1), (3, 2), (3, 3)],
    4: [(8, 1), (9, 1), (10, 1), (4, 2)],
    5: [(11, 1), (2, 5), (2, 6), (2, 7)]
}

# 生成流量文件内容
traffic_file_content = generate_traffic_file(task_deployments)

#生成流量副本，用于观察
with open('../my_file/flow_LLM_BK.txt', 'w') as f:
    # 写入流的数量
    f.write(f"{len(traffic_file_content)}\n")
    for line in traffic_file_content:
        f.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {line[4]} {line[5]} {line[6]:.2f}\n")

print("生成流量副本，用于观察：flow_LLM_BK.txt")

# 生成实际流量
valid_traffic_file_content = []

# 收集有效的流
for line in traffic_file_content:
    if line[1] != line[2]:  # 只记录源节点和目标节点不同的流
        valid_traffic_file_content.append(line)

# 输出生成的流量文件内容
with open('../my_file/flow_LLM.txt', 'w') as f:
    # 写入有效流的数量
    f.write(f"{len(valid_traffic_file_content)}\n")
    
    # 写入有效的流数据
    for line in valid_traffic_file_content:
        f.write(f"{line[0]} {line[1]} {line[2]} {line[3]} {line[4]} {line[5]} {line[6]:.2f}\n")

print("流量文件已生成：flow_LLM.txt")

# 生成任务与流关系的文件，包含每条流的开始时间
task_flow_relations = []

# 遍历流量内容并将流与任务的关系写入文件
for line in traffic_file_content:
    task_id, src_node, dst_node, _, _, data_size, start_time = line
    # 记录任务ID，源节点，目标节点和流的开始时间
    task_flow_relations.append((task_id, src_node, dst_node, data_size, start_time))

# 对任务ID进行排序，确保按任务ID的顺序排列
task_flow_relations.sort(key=lambda x: x[0])

# 输出任务与流的关系到一个文件
with open('../my_file/task_flow_relations.txt', 'w') as f:
    f.write(f"任务ID  源节点  目标节点  数据大小  开始时间\n")
    for line in task_flow_relations:
        f.write(f"{line[0]}    {line[1]}    {line[2]}    {line[3]}    {line[4]:.2f} \n")

print("任务与流的关系文件已生成：task_flow_relations.txt")
