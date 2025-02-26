import matplotlib.pyplot as plt

# List of file paths
file_paths = [
    "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_fairness/result-timely.1",  # Replace with the path to your first file
    "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_fairness/result-timely.2",  # Replace with the path to your second file
    "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_fairness/result-timely.3",  # Replace with the path to your third file
    "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_fairness/result-timely.4"   # Replace with the path to your fourth file
]

# Initialize storage for data
flow_data = {}

# Process each file
for file_index, file_path in enumerate(file_paths):
    with open(file_path, "r") as file:
        for line in file:
            parts = line.split()
            if len(parts) < 5:
                continue
            
            # Extract source, throughput, and time
            src = int(parts[1])  # Src ID
            throughput = float(parts[5]) / 1e9  # Convert to Gbps
            time = float(parts[7]) * 1000  # Convert to milliseconds
            
            # Use (file_index, src) as key to differentiate flows across files
            key = (file_index, src)
            if key not in flow_data:
                flow_data[key] = {"time": [], "throughput": []}
            flow_data[key]["time"].append(time)
            flow_data[key]["throughput"].append(throughput)

# Plot the data
plt.figure(figsize=(12, 7))
for (file_index, src), data in flow_data.items():
    plt.plot(
        data["time"], 
        data["throughput"], 
        label=f"File {file_index + 1} - Flow {src + 1}", 
        marker='o', 
        markersize=1
    )

# Customize plot
plt.xlabel("Times (ms)")
plt.ylabel("Throughput (Gbps)")
plt.title("Throughput vs Time for Each Flow (Across Files)")
plt.legend()
plt.grid()
plt.show()
