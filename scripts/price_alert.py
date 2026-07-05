#!/usr/bin/env python3
"""
🔔 price_alert.py — Price Alert Monitor

Monitor harga token real-time, kirim alert ke Discord/Telegram
saat harga reach target di atas/bawah.

Usage:
    python price_alert.py --mint <MINT> --above 0.001 --below 0.0005 --discord <webhook>
    python price_alert.py --config alerts.json

Config format (alerts.json):
    {
        "alerts": [
            {"mint": "...", "label": "BONK", "above": 0.00003, "below": 0.00002, "webhook": "https://..."}
        ],
        "interval": 30
    }

Dependencies:
    pip install requests
"""
import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

import requests

JUPITER_PRICE_API = "https://price.jup.ag/v6/price"


def get_price(mint: str) -> float:
    """Get current USD price."""
    try:
        resp = requests.get(JUPITER_PRICE_API, params={"ids": mint}, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", {}).get(mint)
        return float(data.get("price", 0)) if data else 0.0
    except Exception:
        return 0.0


def send_alert(webhook_type: str, webhook_url: str, content: str):
    """Send alert via Discord or Telegram."""
    try:
        if webhook_type == "discord":
            requests.post(webhook_url, json={"content": content}, timeout=10)
        elif webhook_type == "telegram":
            # Format: https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<ID>
            requests.post(webhook_url, json={"text": content}, timeout=10)
    except Exception as e:
        print(f"⚠️ Alert send failed: {e}")


def detect_webhook_type(url: str) -> str:
    if "discord.com" in url or "discordapp.com" in url:
        return "discord"
    if "telegram" in url:
        return "telegram"
    return "discord"  # default


def check_alert(alert: dict) -> str | None:
    """
    Check single alert condition.
    Returns alert message or None.
    """
    mint = alert["mint"]
    label = alert.get("label", mint[:6])
    price = get_price(mint)
    if price == 0:
        return None

    above = alert.get("above")
    below = alert.get("below")

    msg = None
    if above is not None and price >= above:
        msg = f"🚨 {label} ABOVE target!\n   Current: ${price:.8f}\n   Target:  ${above:.8f}"
    elif below is not None and price <= below:
        msg = f"🚨 {label} BELOW target!\n   Current: ${price:.8f}\n   Target:  ${below:.8f}"

    return msg


def run_loop(alerts: list, interval: int):
    """Main monitoring loop."""
    print(f"\n🔔 Price Alert Monitor")
    print(f"   {len(alerts)} alert(s) | Interval: {interval}s")
    print(f"   Press Ctrl+C to stop\n")

    triggered = set()  # avoid duplicate alerts per session

    while True:
        try:
            for i, alert in enumerate(alerts):
                msg = check_alert(alert)
                if msg:
                    key = f"{i}-{alert.get('above')}-{alert.get('below')}"
                    if key not in triggered:
                        triggered.add(key)
                        ts = datetime.now().strftime("%H:%M:%S")
                        full_msg = f"[{ts}] {msg}"
                        print(f"  {full_msg.replace(chr(10), ' ')}")
                        webhook_url = alert.get("webhook") or os.environ.get("DISCORD_WEBHOOK_URL")
                        if webhook_url:
                            wtype = detect_webhook_type(webhook_url)
                            send_alert(wtype, webhook_url, full_msg)
                else:
                    key = f"{i}-{alert.get('above')}-{alert.get('below')}"
                    triggered.discard(key)

            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Stopped.")
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Price alert monitor")
    parser.add_argument("--mint", help="Token mint address")
    parser.add_argument("--label", default="Token", help="Token label")
    parser.add_argument("--above", type=float, help="Alert when price >= this value")
    parser.add_argument("--below", type=float, help="Alert when price <= this value")
    parser.add_argument("--interval", type=int, default=30, help="Check interval (seconds)")
    parser.add_argument("--discord", help="Discord webhook URL")
    parser.add_argument("--config", help="Load multiple alerts from JSON config")

    args = parser.parse_args()

    if args.config:
        config = json.loads(Path(args.config).read_text())
        alerts = config["alerts"]
        interval = config.get("interval", args.interval)
    elif args.mint:
        alerts = [{
            "mint": args.mint,
            "label": args.label,
            "above": args.above,
            "below": args.below,
            "webhook": args.discord,
        }]
        interval = args.interval
    else:
        parser.print_help()
        sys.exit(1)

    run_loop(alerts, interval)


if __name__ == "__main__":
    main()
