#!/bin/bash

# 定义文件路径
flow_file="/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/flow-burstExp.txt"
fct_file="/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/dump_burst/fct.txt"
output_txt="/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/experiment_results.txt"

# 初始化 TXT 文件
echo "Flow Size (Bytes), FCT (ns) Flow 1, Standalone FCT (ns) Flow 1, FCT (ns) Flow 2, Standalone FCT (ns) Flow 2, FCT (ns) Flow 3, Standalone FCT (ns) Flow 3" > $output_txt

# 定义流的大小范围：972800B 到 50MB，每次递增 45KB
start_size=972800   # 972800B (大约 950KB)
end_size=52428800 # 50MB
increment=46080   # 每次增加45KB

# 进行实验循环
for size in $(seq $start_size $increment $end_size); do
    # 更新流文件中的第一条流的大小
    sed -i "2s/\([^\ ]*\ [^\ ]*\ [^\ ]*\ [^\ ]*\ \)[^ ]*/\1$size/" $flow_file
    
    # 运行仿真
    ./script-burst.sh yes no
    
    # 等待15秒确保仿真结束并稳定数据
    sleep 15

    # 提取 FCT 数据并记录结果
    while read -r line; do
        # 解析 FCT 文件中的每一行
        sip=$(echo $line | awk '{print $1}')
        dip=$(echo $line | awk '{print $2}')
        sport=$(echo $line | awk '{print $3}')
        dport=$(echo $line | awk '{print $4}')
        size_b=$(echo $line | awk '{print $5}')
        start_time=$(echo $line | awk '{print $6}')
        fct=$(echo $line | awk '{print $7}')
        standalone_fct=$(echo $line | awk '{print $8}')

        # 获取流编号，流编号是根据 sip、sport 匹配的
        if [[ "$sip" == "0b000101" ]]; then
            flow1_fct=$fct
            flow1_standalone_fct=$standalone_fct
        elif [[ "$sip" == "0b000301" ]]; then
            flow2_fct=$fct
            flow2_standalone_fct=$standalone_fct
        elif [[ "$sip" == "0b000401" ]]; then
            flow3_fct=$fct
            flow3_standalone_fct=$standalone_fct
        fi
    done < $fct_file

    # 将结果追加到 TXT 文件中
    echo "$size, $flow1_fct, $flow1_standalone_fct, $flow2_fct, $flow2_standalone_fct, $flow3_fct, $flow3_standalone_fct" >> $output_txt

    # 输出当前实验结果
    echo "Experiment with flow size $size Bytes completed."
done

echo "All experiments are completed. Results have been saved to $output_txt."
