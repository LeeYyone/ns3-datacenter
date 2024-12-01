import matplotlib.pyplot as plt

# List of file paths
file_paths = ["/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-dcqcn.burst",
             "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-dctcp.burst",
             "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-hpcc.burst",
             "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-powerInt.burst",
             "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-timely.burst"]  # Replace with actual file paths
algorithm_names = ["DCQCN", "DCTCP", "HPCC", "PowerInt", "Timely"]

# Initialize storage for data
all_times = []
all_qlens = []

# Process each file
for i, file_path in enumerate(file_paths):
    times = []
    qlens = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            times.append(float(parts[11]))  # Time
            qlens.append(int(parts[9]))   # Queue Length
    all_times.append(times)
    all_qlens.append(qlens)

# Plot Queue Length vs Time for all files
plt.figure(figsize=(10, 5))
for i in range(len(file_paths)):
    plt.plot(all_times[i], all_qlens[i], label=algorithm_names[i], linestyle='-', marker='o', markersize=1)
plt.xlabel('Time (s)')
plt.ylabel('Queue Length (KB)')
plt.title('Queue Length vs Time')
#plt.xlim(0.1499, 0.152)  # Set x-axis limits
plt.grid()
plt.legend()
plt.show()
