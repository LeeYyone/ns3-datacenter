import matplotlib.pyplot as plt

# # List of file paths
# file_paths = ["/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-dcqcn.burst",
#              "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-dctcp.burst",
#              "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-hpcc.burst",
#              "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-powerInt.burst",
#              "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-timely.burst"]  # Replace with actual file paths
file_paths = [
    "/home/yone/ns3-datacenter/simulator/ns-3.39/examples/PowerTCP/results_burst/result-dcqcn.burst"
    ]
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
            times.append(float(parts[13]))  # Time
            qlens.append(int(parts[11])/1024/1024)   # Queue Length
    all_times.append(times)
    all_qlens.append(qlens)

# Plot Queue Length vs Time for all files
plt.figure(figsize=(10, 5))
for i in range(len(file_paths)):
    plt.plot(all_times[i], all_qlens[i], label=algorithm_names[i], linestyle='-', marker='o', markersize=1)
plt.xlabel('Time (s)')
plt.ylabel('Queue Length (MB)')
plt.title('Queue Length vs Time')
#plt.xlim(2.6995, 2.7010)  # Set x-axis limits
# plt.xlim(0.89975, 0.9009)  # Set x-axis limits
# plt.xlim(0.149, 0.152)
# plt.xlim(0.098, 0.103)  # Set x-axis limits
# plt.xlim(0.398, 0.403)  # Set x-axis limits
plt.grid()
plt.legend()
plt.savefig("qlen.png")
