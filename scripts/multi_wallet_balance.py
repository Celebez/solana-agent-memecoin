#!/usr/bin/env python3
"""
💰 multi_wallet_balance.py — Quick Multi-Wallet Balance Check

Cepat cek SOL balance dari banyak wallet sekaligus. Cocok untuk monitoring
cold storage + hot wallet + trading wallet dalam 1 command.

Usage:
    python multi_wallet_balance.py <WALLET_1> <WALLET_2> ...
    python multi_wallet_balance.py --file wallets.txt [--label "Main,Cold,Trading"]
    cat wallets.txt | python multi_wallet_balance.py -

Dependencies:
    pip install requests
"""
import os
import sys
import json
import argparse
from datetime import datetime

import requests

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
JUPITER_PRICE_API = "https://price.jup.ag/v6/price"


def rpc_batch(items: list) -> list:
    """Send batch RPC request."""
    if not HELIUS_API_KEY:
        print("❌ HELIUS_API_KEY required")
        sys.exit(1)
    payload = [{"jsonrpc": "2.0", "id": i, "method": "getBalance", "params": [addr]} for i, addr in enumerate(items)]
    try:
        resp = requests.post(HELIUS_RPC, json=payload, timeout=20)
        resp.raise_for_status()
        results = resp.json()
        return [int(r.get("result", {}).get("value", 0)) / 1e9 for r in results]
    except Exception as e:
        print(f"❌ RPC batch error: {e}")
        return [0.0] * len(items)


def get_sol_price() -> float:
    """Get current SOL price."""
    try:
        resp = requests.get(JUPITER_PRICE_API, params={"ids": "So11111111111111111111111111111111111111112"}, timeout=10)
        data = resp.json().get("data", {}).get("So11111111111111111111111111111111111111112")
        return float(data.get("price", 0)) if data else 0.0
    except Exception:
        return 0.0


def main():
    parser = argparse.ArgumentParser(description="Multi-wallet SOL balance check")
    parser.add_argument("wallets", nargs="*", help="Wallet addresses (or '-' for stdin)")
    parser.add_argument("--file", help="File with one wallet per line")
    parser.add_argument("--label", help="Comma-separated labels matching wallets")
    parser.add_argument("--no-usd", action="store_true", help="Skip USD conversion")
    args = parser.parse_args()

    # Load wallets
    wallets = []
    if args.file:
        with open(args.file) as f:
            wallets = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    elif args.wallets and args.wallets[0] == "-":
        wallets = [line.strip() for line in sys.stdin if line.strip()]
    elif args.wallets:
        wallets = args.wallets

    if not wallets:
        parser.print_help()
        sys.exit(1)

    labels = args.label.split(",") if args.label else [f"Wallet-{i+1}" for i in range(len(wallets))]
    if len(labels) != len(wallets):
        print("❌ Number of labels must match number of wallets")
        sys.exit(1)

    # Get balances in batch
    print(f"\n💰 Checking {len(wallets)} wallet(s)...\n")
    balances = rpc_batch(wallets)

    # Get SOL price
    sol_price = 0.0 if args.no_usd else get_sol_price()

    # Display
    print(f"  {'#':<4} {'LABEL':<14} {'ADDRESS':<14} {'BALANCE':<14} {'USD VALUE':<14}")
    print(f"  {'─'*4} {'─'*14} {'─'*14} {'─'*14} {'─'*14}")
    total_sol = 0.0
    for i, (label, addr, bal) in enumerate(zip(labels, wallets, balances), 1):
        total_sol += bal
        usd = bal * sol_price if sol_price else 0
        usd_str = f"${usd:,.2f}" if sol_price else "N/A"
        print(f"  {i:<4} {label[:14]:<14} {addr[:12]:<14} {bal:>12,.4f} {usd_str:>14}")

    print(f"\n  {'TOTAL':<20} {'':<14} {total_sol:>12,.4f} SOL  "
          f"${total_sol * sol_price:,.2f}" if sol_price else f"  {'TOTAL':<20} {'':<14} {total_sol:>12,.4f} SOL")
    print(f"\n  SOL price: ${sol_price:,.2f}" if sol_price else "")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == "__main__":
    main()
