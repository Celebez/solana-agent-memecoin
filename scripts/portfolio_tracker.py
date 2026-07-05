#!/usr/bin/env python3
"""
💼 portfolio_tracker.py — Multi-Wallet Portfolio Tracker

Track holdings dari multiple wallet sekaligus, hitung total value dalam USD.
Output tabel + optional save ke JSON/CSV.

Usage:
    python portfolio_tracker.py <WALLET_1> <WALLET_2> ... [--label "Main,Trading"]
    python portfolio_tracker.py --file wallets.txt [--save portfolio.json]

File format (wallets.txt):
    Main:7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
    Trading:9d8uKJ7AbCdEfGhIjKlMnOpQrStUvWxYz1234567890

Dependencies:
    pip install requests
"""
import os
import sys
import json
import csv
import argparse
from datetime import datetime
from pathlib import Path

import requests

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
JUPITER_PRICE_API = "https://price.jup.ag/v6/price"


def rpc_call(method: str, params: list) -> dict:
    if not HELIUS_API_KEY:
        print("❌ HELIUS_API_KEY tidak di-set!")
        sys.exit(1)
    try:
        resp = requests.post(HELIUS_RPC,
                             json={"jsonrpc": "2.0", "id": "portfolio", "method": method, "params": params},
                             timeout=15)
        resp.raise_for_status()
        return resp.json().get("result") or {}
    except Exception as e:
        print(f"❌ RPC error: {e}")
        return {}


def get_sol_balance(address: str) -> float:
    """Get SOL balance."""
    result = rpc_call("getBalance", [address])
    return result.get("value", 0) / 1e9 if result else 0.0


def get_token_accounts(address: str) -> list:
    """Get all SPL token accounts owned by wallet."""
    result = rpc_call("getTokenAccountsByOwner", [
        address,
        {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
        {"encoding": "jsonParsed"}
    ])
    accounts = (result.get("value") or []) if result else []
    parsed_tokens = []
    for acc in accounts:
        info = acc.get("account", {}).get("data", {}).get("parsed", {}).get("info", {})
        token_amount = info.get("tokenAmount", {})
        ui_amount = float(token_amount.get("uiAmount") or 0)
        if ui_amount > 0:
            parsed_tokens.append({
                "mint": info.get("mint"),
                "amount": ui_amount,
                "decimals": int(token_amount.get("decimals", 0)),
            })
    return parsed_tokens


def get_prices(mints: list) -> dict:
    """Get USD prices dari Jupiter Price API (free, no key)."""
    if not mints:
        return {}
    try:
        resp = requests.get(JUPITER_PRICE_API, params={"ids": ",".join(mints)}, timeout=15)
        resp.raise_for_status()
        data = resp.json().get("data", {})
        return {mint: float(d.get("price", 0)) for mint, d in data.items()}
    except Exception as e:
        print(f"⚠️ Price fetch error: {e}")
        return {}


def track_wallet(label: str, address: str) -> dict:
    """Track single wallet."""
    sol_balance = get_sol_balance(address)
    tokens = get_token_accounts(address)

    mints = ["So11111111111111111111111111111111111111112"] + [t["mint"] for t in tokens]
    prices = get_prices(mints)

    sol_price = prices.get("So11111111111111111111111111111111111111112", 0)
    sol_value = sol_balance * sol_price

    holdings = [{
        "symbol": "SOL",
        "mint": "So11111111111111111111111111111111111111112",
        "amount": sol_balance,
        "price_usd": sol_price,
        "value_usd": sol_value,
    }]

    for t in tokens:
        mint = t["mint"]
        amount = t["amount"]
        price = prices.get(mint, 0)
        value = amount * price
        if value < 0.01:
            continue  # skip dust
        holdings.append({
            "symbol": mint[:6] + "..." + mint[-4:],  # fallback
            "mint": mint,
            "amount": amount,
            "price_usd": price,
            "value_usd": value,
        })

    holdings.sort(key=lambda x: x["value_usd"], reverse=True)
    total_value = sum(h["value_usd"] for h in holdings)

    return {
        "label": label,
        "address": address,
        "total_value_usd": total_value,
        "holdings": holdings,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
    }


def format_report(portfolios: list) -> str:
    """Format portfolio report."""
    grand_total = sum(p["total_value_usd"] for p in portfolios)
    lines = [
        "",
        "═══════════════════════════════════════════════════════════════",
        f"  📊 PORTFOLIO REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  💰 Total: ${grand_total:,.2f} USD across {len(portfolios)} wallet(s)",
        "═══════════════════════════════════════════════════════════════",
    ]

    for p in portfolios:
        lines.append(f"\n  🏷️  {p['label']} ({p['address'][:8]}...{p['address'][-4:]})")
        lines.append(f"      Total: ${p['total_value_usd']:,.2f}")
        lines.append(f"      {'SYMBOL':<14} {'AMOUNT':>14} {'PRICE':>14} {'VALUE':>14}")
        lines.append(f"      {'─'*14} {'─'*14} {'─'*14} {'─'*14}")
        for h in p["holdings"][:20]:
            lines.append(
                f"      {h['symbol'][:14]:<14} "
                f"{h['amount']:>14,.4f} "
                f"${h['price_usd']:>13,.6f} "
                f"${h['value_usd']:>13,.2f}"
            )

    lines.append("\n═══════════════════════════════════════════════════════════════\n")
    return "\n".join(lines)


def load_wallets_file(path: str) -> list:
    """Load wallets from file (label:address per line)."""
    wallets = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                label, addr = line.split(":", 1)
                wallets.append((label.strip(), addr.strip()))
            else:
                wallets.append((f"Wallet-{len(wallets)+1}", line))
    return wallets


def main():
    parser = argparse.ArgumentParser(description="Multi-wallet portfolio tracker")
    parser.add_argument("wallets", nargs="*", help="Wallet addresses")
    parser.add_argument("--label", help="Comma-separated labels matching wallets")
    parser.add_argument("--file", help="File with wallets (label:address per line)")
    parser.add_argument("--save", help="Save report ke JSON file")
    args = parser.parse_args()

    wallet_list = []
    if args.file:
        wallet_list = load_wallets_file(args.file)
    elif args.wallets:
        labels = args.label.split(",") if args.label else [f"Wallet-{i+1}" for i in range(len(args.wallets))]
        if len(labels) != len(args.wallets):
            print("❌ Number of labels must match number of wallets")
            sys.exit(1)
        wallet_list = list(zip(labels, args.wallets))

    if not wallet_list:
        parser.print_help()
        sys.exit(1)

    print(f"\n⏳ Tracking {len(wallet_list)} wallet(s)...")
    portfolios = []
    for label, addr in wallet_list:
        p = track_wallet(label, addr)
        portfolios.append(p)
        print(f"  ✅ {label}: ${p['total_value_usd']:,.2f}")

    print(format_report(portfolios))

    if args.save:
        Path(args.save).write_text(json.dumps(portfolios, indent=2))
        print(f"💾 Saved to {args.save}\n")


if __name__ == "__main__":
    main()
