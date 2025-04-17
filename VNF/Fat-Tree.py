import networkx as nx

def generate_fat_tree(K):
    G = nx.Graph()
    num_pods = K
    num_core = (K // 2) ** 2
    num_agg_per_pod = K // 2
    num_edge_per_pod = K // 2
    num_hosts_per_edge = K // 2

    # Add core switches
    core_switches = [f'c{i}' for i in range(num_core)]
    G.add_nodes_from(core_switches, type='core')

    # Add pods
    for pod in range(num_pods):
        agg_switches = [f'a{pod}_{i}' for i in range(num_agg_per_pod)]
        edge_switches = [f'e{pod}_{i}' for i in range(num_edge_per_pod)]
        G.add_nodes_from(agg_switches, type='agg')
        G.add_nodes_from(edge_switches, type='edge')

        # Connect aggregation to edge switches within pod
        for agg in agg_switches:
            for edge in edge_switches:
                G.add_edge(agg, edge, weight=1)  # Unweighted graph

        # Connect aggregation to core switches
        for i, agg in enumerate(agg_switches):
            core_idx = i * (num_core // num_agg_per_pod)
            G.add_edge(agg, core_switches[core_idx], weight=1)

        # Add hosts
        for e_idx, edge in enumerate(edge_switches):
            hosts = [f'h{pod}_{e_idx}_{i}' for i in range(num_hosts_per_edge)]
            G.add_nodes_from(hosts, type='host')
            for host in hosts:
                G.add_edge(edge, host, weight=1)

    return G

# Generate K=4 fat-tree
G = generate_fat_tree(4)
V_s = [node for node in G.nodes() if G.nodes[node]['type'] != 'host']