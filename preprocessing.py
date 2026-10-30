
import json
import pandas as pd

# Load the match events
with open("events.json", "r", encoding="utf-8") as file:
    events = json.load(file)

df = pd.json_normalize(events)

# Extract all passing events
passes = df[df["type.name"] == "Pass"].copy()

# Keep successful passes only
# In StatsBomb, missing outcome generally means successful
successful_passes = passes[
    passes["pass.outcome.name"].isna()
].copy()

# Remove passes without a recorded receiver
successful_passes = successful_passes.dropna(
    subset=["player.name", "pass.recipient.name"]
)

# Select required columns
clean_data = successful_passes[[
    "team.name",
    "player.name",
    "pass.recipient.name",
    "minute",
    "second"
]].copy()

# Rename columns
clean_data.columns = [
    "team",
    "passer",
    "receiver",
    "minute",
    "second"
]

# Save processed data
clean_data.to_csv("successful_passes.csv", index=False)

print("DATA PREPROCESSING COMPLETED")
print("--------------------------------")

print("Total passes:", len(passes))
print("Successful passes:", len(clean_data))
print("Unsuccessful or excluded passes:",
      len(passes) - len(clean_data))

print("\nSuccessful passes by team:")
print(clean_data["team"].value_counts())

print("\nSample processed data:")
print(clean_data.head(10).to_string(index=False))
