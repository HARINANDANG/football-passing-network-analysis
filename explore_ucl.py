
import pandas as pd
import json

with open("competitions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

ucl = df[
    df["competition_name"].str.contains(
        "Champions League",
        case=False,
        na=False
    )
]

print("\nAVAILABLE UCL SEASONS\n")

print(
    ucl[[
        "competition_id",
        "competition_name",
        "season_id",
        "season_name"
    ]].to_string(index=False)
)
