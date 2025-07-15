import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

def load_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Flatten nested fields like 'actionData.amount'
    df = pd.json_normalize(data)
    return df

def extract_features(df):
    grouped = df.groupby('userWallet')  # Group by correct user field
    features = pd.DataFrame()

    features['total_transactions'] = grouped.size()
    features['num_deposits'] = grouped.apply(lambda x: (x['action'] == 'deposit').sum())
    features['num_borrows'] = grouped.apply(lambda x: (x['action'] == 'borrow').sum())
    features['num_repays'] = grouped.apply(lambda x: (x['action'] == 'repay').sum())
    features['num_redeems'] = grouped.apply(lambda x: (x['action'] == 'redeemunderlying').sum())
    features['num_liquidations'] = grouped.apply(lambda x: (x['action'] == 'liquidationcall').sum())

    # Normalize borrowed/repay amounts by dividing by 1e18 (if in wei)
    features['total_borrow_amount'] = grouped.apply(
        lambda x: x[x['action'] == 'borrow']['actionData.amount'].astype(float).sum() / 1e18
    )
    features['total_repay_amount'] = grouped.apply(
        lambda x: x[x['action'] == 'repay']['actionData.amount'].astype(float).sum() / 1e18
    )

    # Avoid dividing by zero
    features['repay_ratio'] = features['total_repay_amount'] / (features['total_borrow_amount'] + 1e-6)
    features['liquidation_ratio'] = features['num_liquidations'] / (features['total_transactions'] + 1e-6)

    return features.fillna(0)


def calculate_scores(features_df):
    # Completely drop amount-based fields and repay_ratio
    features_df['score_raw'] = (
        features_df['num_deposits'] * 1 +
        features_df['num_borrows'] * 2 +
        features_df['num_repays'] * 3 -
        features_df['num_liquidations'] * 5
    )

    # Fill NaNs if any
    features_df['score_raw'] = features_df['score_raw'].fillna(0)

    # Normalize between 0–1000
    scaler = MinMaxScaler(feature_range=(0, 1000))
    features_df['score'] = scaler.fit_transform(features_df[['score_raw']])
    features_df['score'] = features_df['score'].round(2)

    # Reset index and rename
    score_df = features_df[['score']].reset_index()
    score_df.rename(columns={'userWallet': 'user'}, inplace=True)
    return score_df



def save_scores(score_df, output_path='wallet_scores.csv'):
    score_df.to_csv(output_path, index=False)
    print(f"✅ Scores saved to: {output_path}")

def main():
    input_path = os.path.join('data', 'user_transactions.json')
    df = load_json(input_path)

    # 🧪 Print one row and all column names to check structure
    print(df.head(1))
    print(df.columns)

    # 🧪 Print count of each action type
    print("\nTransaction Action Counts:")
    print(df['action'].value_counts())

    features = extract_features(df)

    # 🧪 View extracted features for debugging
    print("\nExtracted Feature Summary:")
    print(features.describe())

    score_df = calculate_scores(features)
    save_scores(score_df)


if __name__ == "__main__":
    main()
