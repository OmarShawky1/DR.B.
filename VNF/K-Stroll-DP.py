def dp_stroll(G, s, t, k, V_s):
    V_prime = V_s + [s, t]
    sp = dict(nx.all_pairs_shortest_path_length(G))  # Shortest path costs
    c = {(u, v): sp[u][v] for u in V_prime for v in V_prime if u != v}

    INF = float('inf')
    c_dp = {}
    successor = {}

    # Initialize for e=1
    for u in V_prime:
        if u != t:
            c_dp[(u, 1)] = c.get((u, t), INF)
            successor[(u, 1)] = t

    # DP for increasing number of edges
    r = k + 1
    found = False
    while not found:
        for e in range(2, r + 1):
            for u in V_prime:
                if u == t:
                    continue
                for v in V_prime:
                    if v != u and v != t and v not in successor.get((u, e-1), []):
                        cost = c.get((u, v), INF) + c_dp.get((v, e-1), INF)
                        if cost < c_dp.get((u, e), INF):
                            c_dp[(u, e)] = cost
                            successor[(u, e)] = v

        # Check if path has at least k distinct switches
        path = []
        e = r
        u = s
        while e > 0 and (u, e) in successor:
            v = successor[(u, e)]
            path.append(v)
            u = v
            e -= 1
        switches_visited = [node for node in path if node in V_s]
        if len(set(switches_visited)) >= k:
            found = True
        else:
            r += 1

    cost = c_dp.get((s, r), INF)
    return cost