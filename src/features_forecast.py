import pandas as pd
import numpy as np
from datetime import timedelta

# Parameters
INPUT_CSV = "data/processed/google_trends_cleaned_{date}.csv"  # we'll format date
OUTPUT_CSV = "data/ml_dataset.csv"
WINDOW = 7        # days for feature window
FUTURE = 7        # days ahead for label
SPIKE_THRESHOLD = 0.75  # percentile threshold for spike

def compute_features_and_label(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each player and each date where we have enough history and future,
    compute features (last 7-day mean, std, slope, spike count past 30 days, last score)
    and label (1 if next 7-day avg > SPIKE_THRESHOLD quantile of past data).
    """
    records = []
    players = df.columns
    dates = df.index

    # Precomputing global thresholds per player.
    future_avgs = {
        p: df[p].rolling(window=FUTURE).mean().shift(-FUTURE)
        for p in players
    }

    # For each date where window and future windows fit.
    for current_date in dates[WINDOW:-FUTURE]:
        past_window = df.loc[current_date - timedelta(days=WINDOW-1) : current_date]
        for p in players:
            # features.
            last_7 = past_window[p]
            mean_last_7 = last_7.mean()
            std_last_7  = last_7.std()
            # slope via simple linear fit.
            x = np.arange(len(last_7))
            slope_last_7 = np.polyfit(x, last_7.values, 1)[0]
            # spike count past 30 days (>80).
            past_30 = df[p].loc[current_date - timedelta(days=29) : current_date]
            prev_spike_count = (past_30 > 80).sum()
            last_score = last_7.iloc[-1]

            # label: comparing future avg to historical distribution.
            future_avg = future_avgs[p].loc[current_date]
            hist = df[p].rolling(window=30).mean().loc[:current_date].dropna()
            spike_cutoff = hist.quantile(SPIKE_THRESHOLD)
            label = int(future_avg > spike_cutoff)

            records.append({
                "date": current_date,
                "player": p,
                "mean_last_7": mean_last_7,
                "std_last_7": std_last_7,
                "slope_last_7": slope_last_7,
                "prev_spike_count": prev_spike_count,
                "last_score": last_score,
                "label": label
            })

    return pd.DataFrame(records)

def main():
    # Loading cleaned trends.
    today = pd.to_datetime("today").strftime("%Y-%m-%d")
    path = INPUT_CSV.format(date=today)
    df = pd.read_csv(path, index_col=0, parse_dates=True)

    dataset = compute_features_and_label(df)
    dataset.to_csv(OUTPUT_CSV, index=False)
    print(f"[OK] ML dataset saved to {OUTPUT_CSV}. Shape: {dataset.shape}")

if __name__ == "__main__":
    main()