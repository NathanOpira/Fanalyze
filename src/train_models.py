import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path)

    # Drop any rows with missing values just in case
    df.dropna(inplace=True)

    # Features and label
    X = df[["mean_last_7", "std_last_7", "slope_last_7", "prev_spike_count", "last_score"]]
    y = df["label"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test