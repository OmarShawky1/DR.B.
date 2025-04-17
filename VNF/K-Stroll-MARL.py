import numpy as np

def marl_stroll(G, s, t, k, V_s, m=16, max_iter=1000):
    sp = dict(nx.all_pairs_shortest_path_length(G))
    Q = {(u, v): 1 / len(G.nodes()) for u, v in G.edges()}
    Q.update({(v, u): 1 / len(G.nodes()) for u, v in G.edges()})

    # Parameters
    alpha, gamma, delta, beta, W, q0 = 0.1, 0.3, 1, 2, 10, 0.9

    best_cost = float('inf')
    for _ in range(max_iter):
        agents = [{'r': s, 'L': [s], 'l': 0, 'U': set(V_s), 'visited': set()} for _ in range(m)]

        # Visit k switches
        for _ in range(k):
            for agent in agents:
                r = agent['r']
                U_adj = [v for v in G.neighbors(r) if v in agent['U']]
                if not U_adj:
                    agent['l'] = float('inf')
                    break
                q = np.random.rand()
                scores = [(v, (Q.get((r, v), 0) ** delta) / (G[r][v]['weight'] ** beta)) for v in U_adj]
                if q <= q0:
                    s_j = max(scores, key=lambda x: x[1])[0]
                else:
                    total = sum(score[1] for score in scores)
                    probs = [score[1] / total for score in scores]
                    s_j = np.random.choice([v for v, _ in scores], p=probs)
                agent['L'].append(s_j)
                agent['l'] += G[r][s_j]['weight']
                agent['r'] = s_j
                agent['U'].remove(s_j)
                agent['visited'].add(s_j)
                max_Q_next = max(Q.get((s_j, v), 0) for v in G.neighbors(s_j) if v in agent['U']) if agent['U'] else 0
                Q[(r, s_j)] = (1 - alpha) * Q.get((r, s_j), 0) + alpha * gamma * max_Q_next

        # Move to destination
        for agent in agents:
            if agent['l'] == float('inf'):
                continue
            switch_k = agent['r']
            agent['l'] += sp[switch_k][t]
            agent['L'].append(t)

        # Update Q-values for best path
        j_star = np.argmin([agent['l'] for agent in agents])
        l_j_star = agents[j_star]['l']
        L_j_star = agents[j_star]['L']
        if l_j_star < best_cost:
            best_cost = l_j_star
            for i in range(len(L_j_star) - 2):  # Up to switch_k
                u, v = L_j_star[i], L_j_star[i + 1]
                r_uv = W / l_j_star
                max_Q_next = max(Q.get((v, w), 0) for w in G.neighbors(v) if w in V_s)
                Q[(u, v)] = (1 - alpha) * Q.get((u, v), 0) + alpha * (r_uv + gamma * max_Q_next)

    return best_cost