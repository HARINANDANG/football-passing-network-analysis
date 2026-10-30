
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# Load successful passes
df = pd.read_csv("successful_passes.csv")
df.columns = df.columns.str.strip()

# Check required columns
required_columns = ["team", "passer", "receiver"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(
            f"Missing column: {col}. "
            f"Available columns: {df.columns.tolist()}"
        )


def build_passing_network(team_name):
    """
    Create a directed and weighted passing network.

    Nodes: Players
    Edges: Directed passes
    Weight: Number of successful passes
    """

    team_df = df[df["team"] == team_name]

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


def visualize_network(G, team_name):

    if G.number_of_nodes() == 0:
        print(f"No passing data available for {team_name}")
        return

    # Total passing involvement
    node_strength = dict(G.degree(weight="weight"))

    # Node sizes
    node_sizes = [
        500 + node_strength[node] * 45
        for node in G.nodes()
    ]

    # Node positions
    pos = nx.spring_layout(
        G,
        seed=42,
        k=1.5,
        iterations=150,
        weight="weight"
    )

    fig, ax = plt.subplots(figsize=(16, 12))

    # Draw nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color="skyblue",
        edgecolors="black",
        linewidths=1.2,
        ax=ax
    )

    # Draw directed and weighted edges
    for u, v, data in G.edges(data=True):

        weight = data["weight"]

        # Separate opposite-direction edges
        if G.has_edge(v, u):

            if str(u) < str(v):
                rad = 0.22
            else:
                rad = -0.22

        else:
            rad = 0.04

        # Edge thickness represents pass frequency
        edge_width = 0.8 + weight * 0.22

        # Draw arrow showing direction
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            width=edge_width,
            edge_color="dimgray",
            alpha=0.75,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=24,
            connectionstyle=f"arc3,rad={rad}",
            min_source_margin=14,
            min_target_margin=18,
            ax=ax
        )

        # Display numerical edge weight
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels={(u, v): str(weight)},
            font_size=8,
            font_color="darkred",
            rotate=False,
            label_pos=0.5,
            bbox={
                "alpha": 0.85,
                "color": "white",
                "edgecolor": "none",
                "pad": 1.2
            },
            connectionstyle=f"arc3,rad={rad}",
            ax=ax
        )

    # Player labels
    labels = {
        node: str(node).split()[-1]
        for node in G.nodes()
    }

    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        font_size=9,
        font_weight="bold",
        font_color="black",
        ax=ax
    )

    # Graph title
    ax.set_title(
        f"{team_name} Directed, Weighted Passing Network",
        fontsize=18,
        fontweight="bold",
        pad=20
    )

    # Legend / explanation
    ax.text(
        0.5,
        -0.02,
        "Arrow direction = Pass direction | "
        "Edge number = Pass count | "
        "Edge thickness = Pass frequency | "
        "Node size = Passing involvement",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9
    )

    ax.axis("off")
    plt.tight_layout()

    # Save visualization
    filename = (
        team_name.replace(" ", "_")
        + "_passing_network.png"
    )

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    print(f"Saved: {filename}")

    # Verify graph properties
    print("\nTeam:", team_name)
    print("Directed graph:", G.is_directed())
    print(
        "All edges weighted:",
        all(
            "weight" in data
            for _, _, data in G.edges(data=True)
        )
    )
    print("Number of players:", G.number_of_nodes())
    print("Number of connections:", G.number_of_edges())

    plt.show()
    plt.close(fig)


# Main execution
if __name__ == "__main__":

    teams = [
        "Liverpool",
        "Tottenham Hotspur"
    ]

    for team in teams:

        G = build_passing_network(team)

        visualize_network(G, team)
