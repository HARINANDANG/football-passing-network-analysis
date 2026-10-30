
import json
import pandas as pd

with open("matches.json", "r", encoding="utf-8") as file:
    matches = json.load(file)

df = pd.DataFrame(matches)

print("\nAVAILABLE UCL MATCHES\n")

print("Total matches:", len(df))

print(
    df[[
        "match_id",
        "home_team",
        "away_team",
        "match_date"
    ]].to_string(index=False)
)
