#!/usr/bin/env python3
"""
📲 telegram_notifier.py — Telegram Notification Sender

Kirim alert ke Telegram bot (juga support group/channel).
Berbeda dengan discord_notifier.py — pakai Telegram Bot API.

Setup:
1. Chat dengan @BotFather di Telegram
2. /newbot → simpan token
3. Dapatkan chat_id dari @userinfobot atau @get_id_bot
4. export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
5. export TELEGRAM_CHAT_ID="123456789"

Usage:
    python telegram_notifier.py "🚨 Trade executed: BUY 100 SOL"
    python telegram_notifier.py --markdown "*Bold* _italic_ [link](https://solana.com)"

Dependencies:
    pip install requests
"""
import os
import sys
import argparse
import requests

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


def send(text: str, token: str = None, chat_id: str = None,
         parse_mode: str = None, silent: bool = False) -> bool:
    """
    Send message via Telegram bot.

    Args:
        text: Message text (max 4096 chars)
        token: Bot token (or env TELEGRAM_BOT_TOKEN)
        chat_id: Target chat ID (or env TELEGRAM_CHAT_ID)
        parse_mode: 'Markdown', 'MarkdownV2', 'HTML', or None
        silent: Send without notification sound

    Returns:
        True on success
    """
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️  TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID required")
        print("   Setup: https://core.telegram.org/bots/tutorial")
        return False

    url = TELEGRAM_API.format(token=token, method="sendMessage")
    payload = {
        "chat_id": chat_id,
        "text": text[:4096],  # Telegram limit
        "disable_notification": silent,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json()
        if not data.get("ok"):
            print(f"❌ Telegram error: {data.get('description', 'Unknown')}")
            return False
        return True
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Telegram notifier")
    parser.add_argument("message", nargs="+", help="Message text")
    parser.add_argument("--markdown", action="store_true", help="Use Markdown parse mode")
    parser.add_argument("--silent", action="store_true", help="Send silently (no notification)")
    parser.add_argument("--chat-id", help="Override chat_id")
    args = parser.parse_args()

    text = " ".join(args.message)
    parse_mode = "Markdown" if args.markdown else None
    ok = send(text, parse_mode=parse_mode, silent=args.silent, chat_id=args.chat_id)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
