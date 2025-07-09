import pandas as pd
from datetime import datetime

# Getting today's date (same as raw file).
today = datetime.now().strftime("%Y-%m-%d")
raw_file = f"data/raw/google_trends_raw_{today}.csv"
processed_file = f"data/processed/google_trends_cleaned_{today}.csv"

# Loading raw data.
df = pd.read_csv(raw_file, index_col=0, parse_dates=True)

# Merging duplicate player columns (from batching), using max values.
df = df.groupby(df.columns, axis=1).max()

# Normalizing each player's data to a 0–100 scale.
normalized_df = df.apply(lambda x: (x / x.max()) * 100)

# Rounding for cleaner display.
normalized_df = normalized_df.round(2)

# Saving cleaned data.
normalized_df.to_csv(processed_file)

print(f"Cleaned data saved to {processed_file}")