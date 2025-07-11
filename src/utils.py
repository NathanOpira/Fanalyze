import pandas as pd

def get_player_summary(df: pd.DataFrame, player: str, days: int = 7):
    """Return summary stats for a player."""
    latest_data = df[player].tail(days)
    avg_score = round(latest_data.mean(), 1)
    peak_date = df[player].idxmax().strftime('%Y-%m-%d')
    peak_score = int(df[player].max())
    spike_count = int((df[player] > 80).sum())  # customize threshold

    return {
        "name": player,
        "avg_score": avg_score,
        "peak_date": peak_date,
        "peak_score": peak_score,
        "spike_count": spike_count
    }