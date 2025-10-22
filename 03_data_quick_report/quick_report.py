#!/usr/bin/env python3
"""
Quick Sales Report
------------------
Reads a CSV of daily sales and prints a short summary + saves a summary CSV.

Usage:
  python quick_report.py --csv sample_sales.csv
"""
import argparse, pandas as pd

def quick_summary(csv_path: str):
    df = pd.read_csv(csv_path, parse_dates=["date"])
    total = float(df["sales"].sum())
    avg = float(df["sales"].mean())
    by_store = df.groupby("store")["sales"].sum().sort_values(ascending=False)
    by_month = df.groupby(df["date"].dt.to_period("M"))["sales"].sum()
    summary = {
        "total_sales": total,
        "avg_daily_sales": avg,
        "top_store": by_store.idxmax(),
        "top_store_sales": float(by_store.max()),
        "months": by_month.to_dict()
    }
    # Save store summary CSV
    store_summary = by_store.reset_index().rename(columns={"sales":"total_sales"})
    store_summary.to_csv("store_sales_summary.csv", index=False)
    print("== Quick Summary ==")
    print(f"Total sales: {total:,.0f}")
    print(f"Average per day: {avg:,.2f}")
    print("By store:")
    print(store_summary.to_string(index=False))
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to CSV with columns: date, store, sales")
    args = ap.parse_args()
    quick_summary(args.csv)

if __name__ == "__main__":
    main()
