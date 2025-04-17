import time
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

# Define the graph and necessary functions
def dp_stroll(G, s, t, k, V_s):
    # Placeholder implementation
    return np.random.rand() * 100

def marl_stroll(G, s, t, k, V_s):
    # Placeholder implementation
    return np.random.rand() * 100

def main():
    # Create a sample graph
    G = nx.random_graphs.barabasi_albert_graph(10, 2)
    # Add node attributes
    for node in G.nodes():
        G.nodes[node]['type'] = 'host' if node < 6 else 'switch'
    
    # Define V_s (set of VNF servers)
    V_s = [node for node in G.nodes() if G.nodes[node]['type'] == 'host']
    num_runs = 20
    k_values = range(1, 12)
    dp_costs, rl_costs = [], []
    dp_times, rl_times = [], []

    hosts = [node for node in G.nodes() if G.nodes[node]['type'] == 'host']
    for k in k_values:
        dp_cost_sum, rl_cost_sum = 0, 0
        dp_time_sum, rl_time_sum = 0, 0
        for _ in range(num_runs):
            s, t = np.random.choice(hosts, 2, replace=False)
            
            # DP
            start = time.time()
            dp_cost = dp_stroll(G, s, t, k, V_s)
            dp_time_sum += time.time() - start
            dp_cost_sum += dp_cost
            
            # RL
            start = time.time()
            rl_cost = marl_stroll(G, s, t, k, V_s)
            rl_time_sum += time.time() - start
            rl_cost_sum += rl_cost

        dp_costs.append(dp_cost_sum / num_runs)
        rl_costs.append(rl_cost_sum / num_runs)
        dp_times.append(dp_time_sum / num_runs)
        rl_times.append(rl_time_sum / num_runs)

    # Plotting
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(k_values, dp_costs, label='DP')
    plt.plot(k_values, rl_costs, label='RL')
    plt.xlabel('Number of VNFs (k)')
    plt.ylabel('Communication Cost')
    plt.title('Communication Cost Comparison')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(k_values, dp_times, label='DP')
    plt.plot(k_values, rl_times, label='RL')
    plt.xlabel('Number of VNFs (k)')
    plt.ylabel('Execution Time (s)')
    plt.yscale('log')
    plt.title('Execution Time Comparison')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()