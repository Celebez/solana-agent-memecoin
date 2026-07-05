#!/usr/bin/env python3
"""
📊 pnl_calculator.py — Profit & Loss Calculator

Hitung realized & unrealized P&L dari trade history (CSV).
Cocok untuk evaluasi performance trading.

CSV format (trades.csv):
    timestamp,symbol,mint,side,amount,price_usd,fee_usd
    2026-07-01T10:00:00Z,BONK,DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263,buy,1000000,0.000020,0.50
    2026-07-03T15:30:00Z,BONK,DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263,sell,1000000,0.000035,0.50

Usage:
    python pnl_calculator.py trades.csv
    python pnl_calculator.py trades.csv --current-price 0.000040
    python pnl_calculator.py trades.csv --export report.json

Dependencies:
    pip install requests
"""
import os
import sys
import json
import csv
import argparse
from datetime import datetime
from collections import defaultdict
from pathlib import Path

import requests

JUPITER_PRICE_API = "https://price.jup.ag/v6/price"


def parse_trades(csv_path: str) -> list:
    """Parse trades from CSV."""
    trades = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                trades.append({
                    "timestamp": row["timestamp"],
                    "symbol": row["symbol"],
                    "mint": row["mint"],
                    "side": row["side"].lower(),
                    "amount": float(row["amount"]),
                    "price_usd": float(row["price_usd"]),
                    "fee_usd": float(row.get("fee_usd", 0)),
                })
            except (KeyError, ValueError) as e:
                print(f"⚠️ Skip row: {row} — {e}")
    return trades


def fifo_pnl(trades: list) -> dict:
    """
    Calculate FIFO (first-in-first-out) realized P&L.
    Track per-token cost basis.
    """
    # Group by mint
    by_mint = defaultdict(list)
    for t in trades:
        by_mint[t["mint"]].append(t)

    results = {}
    for mint, mint_trades in by_mint.items():
        # Sort by timestamp
        mint_trades.sort(key=lambda t: t["timestamp"])

        # FIFO queue of buy lots
        lots = []  # list of (amount_remaining, cost_per_unit)
        realized = 0.0
        total_bought = 0.0
        total_sold = 0.0
        total_fees = 0.0

        for t in mint_trades:
            total_fees += t["fee_usd"]
            if t["side"] == "buy":
                lots.append([t["amount"], t["price_usd"]])
                total_bought += t["amount"] * t["price_usd"]
            elif t["side"] == "sell":
                remaining = t["amount"]
                proceeds = t["amount"] * t["price_usd"]
                cost = 0.0
                total_sold += t["amount"]

                while remaining > 0 and lots:
                    lot_amount, lot_price = lots[0]
                    consumed = min(remaining, lot_amount)
                    cost += consumed * lot_price
                    lots[0][0] -= consumed
                    remaining -= consumed
                    if lots[0][0] <= 1e-12:
                        lots.pop(0)

                realized += proceeds - cost

        # Remaining position
        position_amount = sum(amt for amt, _ in lots)
        position_cost = sum(amt * price for amt, price in lots)
        avg_cost = position_cost / position_amount if position_amount > 0 else 0

        results[mint] = {
            "symbol": mint_trades[0]["symbol"],
            "realized_pnl": realized,
            "total_bought_usd": total_bought,
            "total_sold_usd": total_sold,
            "total_fees_usd": total_fees,
            "position_amount": position_amount,
            "position_cost_basis": position_cost,
            "avg_cost": avg_cost,
            "num_trades": len(mint_trades),
            "winning_trades": sum(1 for t in mint_trades if t["side"] == "sell"),  # simplified
        }

    return results


def get_current_prices(mints: list) -> dict:
    """Get current prices for unrealized P&L."""
    if not mints:
        return {}
    try:
        resp = requests.get(JUPITER_PRICE_API, params={"ids": ",".join(mints)}, timeout=15)
        data = resp.json().get("data", {})
        return {m: float(d.get("price", 0)) for m, d in data.items()}
    except Exception:
        return {}


def format_report(results: dict, prices: dict) -> str:
    """Format P&L report."""
    total_realized = sum(r["realized_pnl"] for r in results.values())
    total_unrealized = 0.0
    total_fees = sum(r["total_fees_usd"] for r in results.values())
    total_volume = sum(r["total_bought_usd"] + r["total_sold_usd"] for r in results.values())

    lines = [
        "",
        "═══════════════════════════════════════════════════════════════════",
        "  📊 P&L REPORT — " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "═══════════════════════════════════════════════════════════════════",
        "",
        f"  Total Realized P&L : ${total_realized:>+14,.2f}",
        f"  Total Fees Paid    : ${total_fees:>14,.2f}",
        f"  Total Volume       : ${total_volume:>14,.2f}",
        "",
        f"  {'SYMBOL':<10} {'TRADES':<8} {'BOUGHT':<12} {'SOLD':<12} {'REALIZED':<14} {'POSITION':<14} {'UNREALIZED':<12}",
        f"  {'─'*10} {'─'*8} {'─'*12} {'─'*12} {'─'*14} {'─'*14} {'─'*12}",
    ]

    for mint, r in results.items():
        price = prices.get(mint, 0)
        position_amount = r["position_amount"]
        position_value = position_amount * price if price else 0
        unrealized = position_value - r["position_cost_basis"]
        total_unrealized += unrealized

        lines.append(
            f"  {r['symbol'][:10]:<10} {r['num_trades']:<8} "
            f"${r['total_bought_usd']:>10,.2f} ${r['total_sold_usd']:>10,.2f} "
            f"${r['realized_pnl']:>+12,.2f} "
            f"{position_amount:>10,.0f} ${unrealized:>+10,.2f}"
        )

    lines.extend([
        "",
        f"  Total Unrealized P&L : ${total_unrealized:>+14,.2f}",
        f"  TOTAL P&L            : ${total_realized + total_unrealized:>+14,.2f}",
        "═══════════════════════════════════════════════════════════════════",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="P&L calculator for trading history")
    parser.add_argument("csv", help="Path to trades CSV file")
    parser.add_argument("--export", help="Export results to JSON file")
    args = parser.parse_args()

    if not Path(args.csv).exists():
        print(f"❌ File not found: {args.csv}")
        sys.exit(1)

    trades = parse_trades(args.csv)
    if not trades:
        print("❌ No trades found in CSV")
        sys.exit(1)

    print(f"\n📊 Analyzing {len(trades)} trades...")
    results = fifo_pnl(trades)
    mints = [m for m, r in results.items() if r["position_amount"] > 0]
    prices = get_current_prices(mints)

    report = format_report(results, prices)
    print(report)

    if args.export:
        output = {
            "results": results,
            "current_prices": prices,
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }
        Path(args.export).write_text(json.dumps(output, indent=2))
        print(f"💾 Exported to {args.export}\n")


if __name__ == "__main__":
    main()
