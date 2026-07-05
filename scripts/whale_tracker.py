#!/usr/bin/env python3
"""
🐋 whale_tracker.py — Whale Transaction Tracker

Monitor top holders token dan alert saat mereka melakukan transaksi.
Berguna untuk deteksi early dump signal dari insider.

Usage:
    python whale_tracker.py <MINT> [--top 10] [--interval 60] [--discord <webhook>]

Dependencies:
    pip install requests
"""
import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path

import requests

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"


def rpc_call(method: str, params: list) -> dict:
    if not HELIUS_API_KEY:
        print("❌ HELIUS_API_KEY required")
        sys.exit(1)
    try:
        resp = requests.post(HELIUS_RPC,
                             json={"jsonrpc": "2.0", "id": "whale", "method": method, "params": params},
                             timeout=15)
        resp.raise_for_status()
        return resp.json().get("result") or {}
    except Exception as e:
        print(f"❌ RPC error: {e}")
        return {}


def get_top_holders(mint: str, limit: int = 10) -> list:
    """Get top N holders."""
    result = rpc_call("getTokenLargestAccounts", [mint])
    accounts = (result.get("value") or []) if result else []
    return [{"address": a["address"], "amount": float(a.get("uiAmount") or 0)} for a in accounts[:limit]]


def get_recent_signatures(address: str, limit: int = 5) -> list:
    """Get recent signatures for address."""
    result = rpc_call("getSignaturesForAddress", [address, {"limit": limit}])
    return result if isinstance(result, list) else []


def format_alert(holder: dict, tx_sig: str, mint: str) -> str:
    """Format whale alert message."""
    ts = datetime.now().strftime("%H:%M:%S")
    short_addr = holder["address"][:6] + "..." + holder["address"][-4:]
    return (
        f"🐋 [{ts}] Whale activity!\n"
        f"   Holder: {short_addr}\n"
        f"   Balance: {holder['amount']:,.0f} tokens\n"
        f"   TX: https://solscan.io/tx/{tx_sig}"
    )


def send_discord(webhook_url: str, content: str):
    try:
        requests.post(webhook_url, json={"content": content}, timeout=10)
    except Exception as e:
        print(f"⚠️ Discord error: {e}")


def run_loop(mint: str, top_n: int, interval: int, webhook_url: str):
    """Main monitoring loop."""
    print(f"\n🐋 Whale Tracker")
    print(f"   Mint: {mint[:8]}...{mint[-4:]}")
    print(f"   Top {top_n} holders | Interval: {interval}s\n")

    holders = get_top_holders(mint, top_n)
    if not holders:
        print("❌ No holders found")
        sys.exit(1)

    print(f"📊 Tracking {len(holders)} top holders:")
    for i, h in enumerate(holders, 1):
        print(f"   #{i:<3} {h['address'][:8]}...  {h['amount']:,.0f}")
    print()

    seen_sigs = set()
    while True:
        try:
            for holder in holders:
                sigs = get_recent_signatures(holder["address"], limit=5)
                for sig_info in sigs:
                    sig = sig_info.get("signature")
                    if sig and sig not in seen_sigs:
                        seen_sigs.add(sig)
                        msg = format_alert(holder, sig, mint)
                        print(f"  {msg.replace(chr(10), ' | ')}")
                        if webhook_url:
                            send_discord(webhook_url, msg)
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Stopped.")
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Whale transaction tracker")
    parser.add_argument("mint", help="Token mint address")
    parser.add_argument("--top", type=int, default=10, help="Number of top holders to track")
    parser.add_argument("--interval", type=int, default=60, help="Check interval (seconds)")
    parser.add_argument("--discord", help="Discord webhook URL for alerts")
    args = parser.parse_args()

    run_loop(args.mint, args.top, args.interval, args.discord)


if __name__ == "__main__":
    main()
