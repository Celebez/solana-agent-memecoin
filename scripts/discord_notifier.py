#!/usr/bin/env python3
"""
📢 discord_notifier.py — Kirim Alert ke Discord via Webhook

Helper untuk kirim notifikasi ke Discord webhook URL.
Bisa dipanggil dari script lain atau langsung dari command line.

Usage:
    export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
    python discord_notifier.py "🚨 Trade executed: buy 100 SOL"

Or import dari script lain:
    from discord_notifier import send
    send("Hello Discord!", username="My Bot")
"""
import os
import sys
import json
import requests


def send(content: str, username: str = "Solana Watcher",
         webhook_url: str = None) -> bool:
    """
    Kirim message ke Discord webhook.

    Args:
        content: Text content (markdown supported)
        username: Display name untuk bot
        webhook_url: Override webhook URL (default dari env)

    Returns:
        True kalau sukses, False kalau gagal
    """
    webhook_url = webhook_url or os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️  DISCORD_WEBHOOK_URL tidak di-set, skip", file=sys.stderr)
        return False

    payload = {
        "content": content,
        "username": username,
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Discord send failed: {e}", file=sys.stderr)
        return False


def send_embed(title: str, description: str, color: int = 0x21E99A,
               fields: list = None, webhook_url: str = None) -> bool:
    """
    Kirim rich embed ke Discord.

    Args:
        title: Embed title
        description: Embed description
        color: Hex color (default emerald #21E99A)
        fields: List of dicts [{"name": "...", "value": "...", "inline": bool}]
        webhook_url: Override webhook URL

    Returns:
        True kalau sukses
    """
    webhook_url = webhook_url or os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        return False

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "fields": fields or [],
    }

    payload = {
        "username": "Solana Watcher",
        "embeds": [embed],
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Discord embed failed: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <message>")
        print(f"   atau: export DISCORD_WEBHOOK_URL='https://...'")
        sys.exit(1)

    msg = " ".join(sys.argv[1:])
    ok = send(msg)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
