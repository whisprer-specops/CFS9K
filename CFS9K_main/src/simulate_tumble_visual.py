def tumble(wallet_input, depth=4):
    graph = {}
    current = wallet_input
    for _ in range(depth):
        next_wallets = [gen_wallet() for _ in range(3)]
        graph[current] = next_wallets
        current = random.choice(next_wallets)
    return graph
