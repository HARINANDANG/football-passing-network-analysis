
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. LOAD DYNAMIC ANALYSIS DATA
# ==========================================

liverpool = pd.read_csv("Liverpool_dynamic_analysis.csv")

tottenham = pd.read_csv("Tottenham_Hotspur_dynamic_analysis.csv")


# ==========================================
# 2. COMPARE METRICS USING BAR CHARTS
# ==========================================

metrics = [
    ("Successful Passes", "Successful Passes"),
    ("Density", "Network Density"),
    ("Average Clustering", "Average Clustering")
]


for column, title in metrics:

    plt.figure(figsize=(10, 6))

    x = range(len(liverpool))
    width = 0.35

    # Liverpool bars
    plt.bar(
        [i - width / 2 for i in x],
        liverpool[column],
        width,
        label="Liverpool"
    )

    # Tottenham bars
    plt.bar(
        [i + width / 2 for i in x],
        tottenham[column],
        width,
        label="Tottenham"
    )

    plt.xlabel("Match Interval")
    plt.ylabel(title)

    plt.title(
        title + " Comparison",
        fontsize=14,
        fontweight="bold"
    )

    plt.xticks(
        list(x),
        liverpool["Interval"]
    )

    plt.legend()

    plt.tight_layout()

    # Save graph
    filename = title.lower().replace(" ", "_") + "_comparison.png"

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight"
    )

    print("Saved:", filename)

    plt.show()
    plt.close()


# ==========================================
# 3. CALCULATE OVERALL TEAM COMPARISON
# ==========================================

overall = pd.DataFrame({

    "Team": [
        "Liverpool",
        "Tottenham Hotspur"
    ],

    "Total Successful Passes": [
        liverpool["Successful Passes"].sum(),
        tottenham["Successful Passes"].sum()
    ],

    "Average Density": [
        liverpool["Density"].mean(),
        tottenham["Density"].mean()
    ],

    "Average Clustering": [
        liverpool["Average Clustering"].mean(),
        tottenham["Average Clustering"].mean()
    ]

})


# ==========================================
# 4. DISPLAY OVERALL COMPARISON
# ==========================================

print("\n" + "=" * 60)

print("OVERALL TEAM COMPARISON")

print("=" * 60)

print(
    overall.round(3).to_string(index=False)
)


# ==========================================
# 5. SAVE OVERALL COMPARISON TO CSV
# ==========================================

overall.to_csv(
    "overall_team_comparison.csv",
    index=False
)

print("\nOverall comparison saved successfully!")

print("File: overall_team_comparison.csv")


# ==========================================
# 6. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 60)

print("PROJECT COMPARISON COMPLETED")

print("=" * 60)

print("Generated files:")

print("1. successful_passes_comparison.png")
print("2. network_density_comparison.png")
print("3. average_clustering_comparison.png")
print("4. overall_team_comparison.csv")
