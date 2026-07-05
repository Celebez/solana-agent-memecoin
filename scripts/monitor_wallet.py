#!/usr/bin/env python3
"""
👁️ monitor_wallet.py — Monitor Transaksi Wallet Real-time

Monitor transaksi masuk/keluar wallet Solana via Helius RPC.
Bisa juga kirim alert ke Discord via webhook.

Usage:
    export HELIUS_API_KEY="your-key-here"
    python monitor_wallet.py <WALLET_ADDRESS> [--interval 30] [--discord WEBHOOK_URL]

Dependencies:
    pip install requests
"""
import os
import sys
import time
import argparse
import requests
from datetime import datetime

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")


def rpc_call(method: str, params: list) -> dict:
    url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
    payload = {"jsonrpc": "2.0", "id": "monitor", "method": method, "params": params}
    try:
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        return resp.json().get("result", {})
    except Exception as e:
        print(f"❌ RPC error: {e}", file=sys.stderr)
        return {}


def get_balance(address: str) -> float:
    """Get SOL balance."""
    result = rpc_call("getBalance", [address])
    if result:
        return result.get("value", 0) / 1e9
    return 0.0


def get_recent_txs(address: str, limit: int = 10) -> list:
    """Get recent transaction signatures."""
    result = rpc_call("getSignaturesForAddress", [address, {"limit": limit}])
    return result if isinstance(result, list) else []


def format_tx(tx: dict, address: str) -> str:
    """Format transaction for display."""
    sig = tx.get("signature", "?")[:16] + "..."
    ts = tx.get("blockTime", 0)
    when = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else "?"
    err = "❌ FAILED" if tx.get("err") else "✅ OK"
    return f"[{when}] {sig}  {err}  https://solscan.io/tx/{tx.get('signature', '')}"


def send_discord(webhook_url: str, content: str):
    """Send notification to Discord webhook."""
    try:
        requests.post(webhook_url, json={"content": content}, timeout=10)
    except Exception as e:
        print(f"⚠️ Discord send failed: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Monitor Solana wallet transactions")
    parser.add_argument("address", help="Wallet address to monitor")
    parser.add_argument("--interval", type=int, default=30, help="Check interval (seconds)")
    parser.add_argument("--discord", help="Discord webhook URL for alerts")
    args = parser.parse_args()

    if not HELIUS_API_KEY:
        print("❌ HELIUS_API_KEY tidak di-set!")
        sys.exit(1)

    print(f"\n👁️  Monitoring wallet: {args.address}")
    print(f"   Interval: {args.interval}s | Discord: {'ON' if args.discord else 'OFF'}")
    print(f"   Press Ctrl+C to stop\n")

    seen_sigs = set()
    while True:
        try:
            balance = get_balance(args.address)
            txs = get_recent_txs(args.address)

            print(f"💰 Balance: {balance:.6f} SOL  |  Txs: {len(txs)}  |  {datetime.now().strftime('%H:%M:%S')}")

            for tx in txs:
                sig = tx.get("signature")
                if sig and sig not in seen_sigs:
                    seen_sigs.add(sig)
                    msg = f"🔔 New TX: {format_tx(tx, args.address)}"
                    print(f"  {msg}")
                    if args.discord:
                        send_discord(args.discord, f"**{args.address[:8]}...**\n{msg}")

            time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n\n👋 Stopped.")
            sys.exit(0)
        except Exception as e:
            print(f"⚠️ Error: {e}", file=sys.stderr)
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
