import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_distribution(csv_path='wallet_scores.csv'):
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(10, 6))
    bins = [i for i in range(0, 1100, 100)]
    sns.histplot(df['score'], bins=bins, kde=False, color='skyblue', edgecolor='black')
    plt.title("Distribution of Wallet Credit Scores")
    plt.xlabel("Score Range")
    plt.ylabel("Number of Wallets")
    plt.xticks(bins)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("score_distribution.png")
    plt.show()

if __name__ == "__main__":
    plot_distribution()
