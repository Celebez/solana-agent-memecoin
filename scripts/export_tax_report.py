#!/usr/bin/env python3
"""
📤 export_tax_report.py — Export Trade History untuk Tax Reporting

Aggregate trade history dari Phantom/Birdeye CSV exports jadi
format yang bisa di-import ke tax tool (Koinly, CoinTracker, dll).

Output formats:
- Koinly Universal CSV
- Generic FIFO CSV

Usage:
    python export_tax_report.py --input trades.csv --format koinly --output 2026_koinly.csv
    python export_tax_report.py --input trades.csv --format generic --output 2026_report.csv

Dependencies:
    pip install requests
"""
import os
import sys
import csv
import json
import argparse
from datetime import datetime
from pathlib import Path


def read_input_csv(path: str) -> list:
    """Read input trades CSV."""
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def export_koinly(rows: list, output_path: str):
    """
    Export to Koinly Universal CSV format.

    Koinly columns:
    Date, Sent Amount, Sent Currency, Received Amount, Received Currency,
    Fee Amount, Fee Currency, Net Worth Amount, Net Worth Currency,
    Label, Description, TxHash
    """
    fieldnames = [
        "Date", "Sent Amount", "Sent Currency", "Received Amount",
        "Received Currency", "Fee Amount", "Fee Currency", "Net Worth Amount",
        "Net Worth Currency", "Label", "Description", "TxHash"
    ]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            timestamp = row.get("timestamp", "")
            symbol = row.get("symbol", "")
            side = row.get("side", "").lower()
            amount = row.get("amount", "0")
            price = row.get("price_usd", "0")
            fee = row.get("fee_usd", "0")

            try:
                amount_f = float(amount)
                price_f = float(price)
                fee_f = float(fee)
            except ValueError:
                continue

            total_usd = amount_f * price_f

            if side == "buy":
                writer.writerow({
                    "Date": timestamp,
                    "Sent Amount": total_usd,
                    "Sent Currency": "USD",
                    "Received Amount": amount_f,
                    "Received Currency": symbol,
                    "Fee Amount": fee_f,
                    "Fee Currency": "USD",
                    "Net Worth Amount": total_usd,
                    "Net Worth Currency": "USD",
                    "Label": "buy",
                    "Description": f"Buy {symbol}",
                    "TxHash": row.get("tx_hash", ""),
                })
            elif side == "sell":
                writer.writerow({
                    "Date": timestamp,
                    "Sent Amount": amount_f,
                    "Sent Currency": symbol,
                    "Received Amount": total_usd,
                    "Received Currency": "USD",
                    "Fee Amount": fee_f,
                    "Fee Currency": "USD",
                    "Net Worth Amount": total_usd,
                    "Net Worth Currency": "USD",
                    "Label": "sell",
                    "Description": f"Sell {symbol}",
                    "TxHash": row.get("tx_hash", ""),
                })

    print(f"✅ Koinly format exported: {output_path}")


def export_generic(rows: list, output_path: str):
    """Export to generic FIFO format."""
    fieldnames = [
        "date", "type", "asset", "amount", "price_per_unit",
        "total_value_usd", "fee_usd", "cost_basis_usd", "realized_pnl_usd",
        "tx_hash", "notes"
    ]

    # Simplified FIFO calc
    lots = {}  # asset -> [(amount_remaining, cost_per_unit)]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in sorted(rows, key=lambda r: r.get("timestamp", "")):
            symbol = row.get("symbol", "")
            side = row.get("side", "").lower()
            try:
                amount = float(row.get("amount", 0))
                price = float(row.get("price_usd", 0))
                fee = float(row.get("fee_usd", 0))
            except ValueError:
                continue

            total = amount * price
            cost_basis = 0.0
            realized = 0.0

            if symbol not in lots:
                lots[symbol] = []

            if side == "buy":
                lots[symbol].append([amount, price])
                writer.writerow({
                    "date": row.get("timestamp", ""),
                    "type": "BUY",
                    "asset": symbol,
                    "amount": amount,
                    "price_per_unit": price,
                    "total_value_usd": total,
                    "fee_usd": fee,
                    "cost_basis_usd": total,
                    "realized_pnl_usd": 0.0,
                    "tx_hash": row.get("tx_hash", ""),
                    "notes": "",
                })
            elif side == "sell":
                remaining = amount
                while remaining > 0 and lots[symbol]:
                    lot_amount, lot_price = lots[symbol][0]
                    consumed = min(remaining, lot_amount)
                    cost_basis += consumed * lot_price
                    realized += consumed * (price - lot_price)
                    lots[symbol][0][0] -= consumed
                    remaining -= consumed
                    if lots[symbol][0][0] <= 1e-12:
                        lots[symbol].pop(0)

                writer.writerow({
                    "date": row.get("timestamp", ""),
                    "type": "SELL",
                    "asset": symbol,
                    "amount": amount,
                    "price_per_unit": price,
                    "total_value_usd": total,
                    "fee_usd": fee,
                    "cost_basis_usd": cost_basis,
                    "realized_pnl_usd": realized - fee,
                    "tx_hash": row.get("tx_hash", ""),
                    "notes": "",
                })

    print(f"✅ Generic format exported: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Export trade history untuk tax reporting")
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--format", choices=["koinly", "generic"], default="koinly",
                        help="Output format")
    parser.add_argument("--output", required=True, help="Output CSV file")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"❌ Input not found: {args.input}")
        sys.exit(1)

    rows = read_input_csv(args.input)
    print(f"\n📤 Exporting {len(rows)} trades to {args.format} format...")

    if args.format == "koinly":
        export_koinly(rows, args.output)
    else:
        export_generic(rows, args.output)

    print(f"\n💡 Next steps:")
    print(f"   1. Buka https://koinly.io (atau CoinTracker)")
    print(f"   2. Import file: {args.output}")
    print(f"   3. Review & generate tax report PDF\n")


if __name__ == "__main__":
    main()
