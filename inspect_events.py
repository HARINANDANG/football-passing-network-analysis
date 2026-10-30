
import json
import pandas as pd

# Load match events
with open("events.json", "r", encoding="utf-8") as file:
    events = json.load(file)

# Convert events into a DataFrame
df = pd.json_normalize(events)

print("TOTAL EVENTS:", len(df))

print("\nTEAMS IN THE MATCH:")
print(df["team.name"].dropna().unique())

print("\nEVENT TYPES:")
print(df["type.name"].value_counts())

print("\nPASS EVENTS:")
passes = df[df["type.name"] == "Pass"]

print("Total passes:", len(passes))

print("\nSAMPLE PASS DATA:")
print(
    passes[[
        "team.name",
        "player.name",
        "pass.recipient.name",
        "pass.outcome.name"
    ]].head(10).to_string(index=False)
)
