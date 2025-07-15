# 💳 DeFi Wallet Credit Scoring - Aave V2

## 📌 Objective
This project assigns a **credit score (0–1000)** to each wallet address that interacted with the Aave V2 protocol...

## ⚙️ Features Extracted Per Wallet
- total_transactions
- num_deposits
- num_borrows
- ...

## 🧮 Scoring Logic
score_raw = (deposits + 2 * repays - 3 * liquidations + repay_ratio * 10)

## 🚀 How to Run
python src/score_generator.py
