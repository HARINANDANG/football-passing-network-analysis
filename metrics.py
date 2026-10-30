
import pandas as pd
import networkx as nx
from network_builder import build_passing_network


def calculate_metrics(G):

    players = list(G.nodes())

    # 1. Degree centrality
    in_degree = nx.in_degree_centrality(G)
    out_degree = nx.out_degree_centrality(G)

    # 2. Weighted passing involvement
    in_strength = dict(G.in_degree(weight="weight"))
    out_strength = dict(G.out_degree(weight="weight"))

    # 3. Convert pass frequency into distance
    H = G.copy()

    for u, v, data in H.edges(data=True):
        data["distance"] = 1 / data["weight"]

    # 4. Betweenness centrality
    betweenness = nx.betweenness_centrality(
        H,
        weight="distance",
        normalized=True
    )

    # 5. Incoming closeness centrality
    incoming_closeness = nx.closeness_centrality(
        H,
        distance="distance"
    )

    # 6. Outgoing closeness centrality
    outgoing_closeness = nx.closeness_centrality(
        H.reverse(copy=True),
        distance="distance"
    )

    # 7. Eigenvector centrality
    eigenvector = nx.eigenvector_centrality(
        G,
        max_iter=1000,
        weight="weight"
    )

    # 8. PageRank
    pagerank = nx.pagerank(
        G,
        weight="weight"
    )

    # Convert all metrics into Series indexed by player
    results = pd.DataFrame(index=players)

    results["In Degree"] = pd.Series(in_degree)
    results["Out Degree"] = pd.Series(out_degree)

    results["In Strength"] = pd.Series(in_strength)
    results["Out Strength"] = pd.Series(out_strength)

    results["Betweenness"] = pd.Series(betweenness)

    results["Incoming Closeness"] = pd.Series(
        incoming_closeness
    )

    results["Outgoing Closeness"] = pd.Series(
        outgoing_closeness
    )

    results["Eigenvector"] = pd.Series(eigenvector)
    results["PageRank"] = pd.Series(pagerank)

    # Add player names as a column
    results.index.name = "Player"
    results = results.reset_index()

    # Sort by PageRank
    results = results.sort_values(
        by="PageRank",
        ascending=False
    )

    return results


if __name__ == "__main__":

    teams = [
        "Liverpool",
        "Tottenham Hotspur"
    ]

    for team in teams:

        print("\n" + "=" * 50)
        print(team.upper())
        print("=" * 50)

        G = build_passing_network(team)

        metrics_df = calculate_metrics(G)

        print(
            metrics_df.head(5).to_string(index=False)
        )

        filename = team.replace(" ", "_") + "_metrics.csv"

        metrics_df.to_csv(filename, index=False)

        print("\nSaved:", filename)
