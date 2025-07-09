import os
import pandas as pd
from datetime import datetime
from pytrends.request import TrendReq

# Initializing pytrends.
pytrends = TrendReq(hl='en-US', tz=360)

# List of players to track.
players = [
    "Ilaix Moriba", "Kamaldeen Sulemana", "Carlos Baleba", "Bryan Mbuemo",
    "Ismaila Sarr", "Mohamed Salah", "Samuel Chukwueze", "Antoine Semenyo",
    "Achraf Hakimi", "Ademola Lookman", "Serhou Guirassy", "Bilal El Khannouss", "Mohammed Kudus"
]

# Google Trends allows max 5 terms at once.
batch_size = 5
batches = [players[i:i + batch_size] for i in range(0, len(players), batch_size)]

# Fetching trends per batch.
all_data = []

for batch in batches:
    try:
        pytrends.build_payload(batch, cat=0, timeframe='today 3-m', geo='', gprop='')
        df = pytrends.interest_over_time()
        if not df.empty:
            df = df.drop(columns=["isPartial"], errors="ignore")
            all_data.append(df)
    except Exception as e:
        print(f"⚠ Error fetching batch {batch}: {e}")

# Combining into one DataFrame.
if all_data:
    combined_df = pd.concat(all_data, axis=1)
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = f"data/raw/google_trends_raw_{today}.csv"
    combined_df.to_csv(output_file)
    print(f"Trends data saved to {output_file}")
else:
    print("No data fetched.")