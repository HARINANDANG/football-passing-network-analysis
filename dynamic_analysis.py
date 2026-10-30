
import pandas as pd
import networkx as nx


# Load successful passes
df = pd.read_csv("successful_passes.csv")

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Define match intervals
intervals = [
    (0, 15, "0-15"),
    (15, 30, "15-30"),
    (30, 45, "30-45"),
    (45, 60, "45-60"),
    (60, 75, "60-75"),
    (75, float("inf"), "75+")
]


def build_interval_network(team_df):

    G = nx.DiGraph()

    for _, row in team_df.iterrows():

        passer = row["passer"]
        receiver = row["receiver"]

        if pd.isna(passer) or pd.isna(receiver):
            continue

        if G.has_edge(passer, receiver):
            G[passer][receiver]["weight"] += 1

        else:
            G.add_edge(
                passer,
                receiver,
                weight=1
            )

    return G


def analyze_interval(G, interval_name, pass_count):

    players = G.number_of_nodes()
    connections = G.number_of_edges()

    # Network density
    density = nx.density(G) if players > 1 else 0

    # Average clustering coefficient
    if players > 0:
        undirected_G = G.to_undirected()
        clustering = nx.average_clustering(undirected_G)
    else:
        clustering = 0

    # Weakly connected components
    components = (
        nx.number_weakly_connected_components(G)
        if players > 0 else 0
    )

    return {
        "Interval": interval_name,
        "Successful Passes": pass_count,
        "Active Players": players,
        "Connections": connections,
        "Density": density,
        "Average Clustering": clustering,
        "Weak Components": components
    }


def dynamic_analysis(team_name):

    team_df = df[df["team"] == team_name].copy()

    results = []

    for start, end, label in intervals:

        # Select passes within the interval
        if end == float("inf"):
            interval_df = team_df[
                team_df["minute"] >= start
            ]
        else:
            interval_df = team_df[
                (team_df["minute"] >= start) &
                (team_df["minute"] < end)
            ]

        # Build network for this interval
        G = build_interval_network(interval_df)

        # Calculate metrics
        result = analyze_interval(
            G,
            label,
            len(interval_df)
        )

        results.append(result)

    return pd.DataFrame(results)


if __name__ == "__main__":

    teams = [
        "Liverpool",
        "Tottenham Hotspur"
    ]

    for team in teams:

        print("\n" + "=" * 60)
        print(team.upper(), "- DYNAMIC NETWORK ANALYSIS")
        print("=" * 60)

        result_df = dynamic_analysis(team)

        print(result_df.to_string(index=False))

        filename = (
            team.replace(" ", "_") +
            "_dynamic_analysis.csv"
        )

        result_df.to_csv(filename, index=False)

        print("\nSaved:", filename)
