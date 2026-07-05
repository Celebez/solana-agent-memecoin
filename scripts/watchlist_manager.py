#!/usr/bin/env python3
"""
⭐ watchlist_manager.py — Watchlist Manager

CRUD watchlist token ke JSON file. Compatible dengan price_alert.py & portfolio_tracker.py.

Usage:
    python watchlist_manager.py add <MINT> [--label "BONK"] [--note "Watching for breakout"]
    python watchlist_manager.py remove <MINT>
    python watchlist_manager.py list
    python watchlist_manager.py update <MINT> --label NEW_LABEL
    python watchlist_manager.py clear
    python watchlist_manager.py import-twitter <HANDLE>  # scan followed accounts
"""
import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

WATCHLIST_FILE = Path.home() / ".solana_watchlist.json"


def load_watchlist() -> list:
    """Load watchlist dari file."""
    if WATCHLIST_FILE.exists():
        return json.loads(WATCHLIST_FILE.read_text())
    return []


def save_watchlist(items: list):
    """Save watchlist ke file."""
    WATCHLIST_FILE.write_text(json.dumps(items, indent=2))
    os.chmod(WATCHLIST_FILE, 0o600)


def add_item(mint: str, label: str = "", note: str = "", tags: list = None) -> dict:
    """Add token to watchlist."""
    items = load_watchlist()
    # Check duplicate
    if any(i["mint"] == mint for i in items):
        print(f"⚠️  {mint} sudah ada di watchlist")
        return None
    item = {
        "mint": mint,
        "label": label or mint[:6],
        "note": note,
        "tags": tags or [],
        "added_at": datetime.utcnow().isoformat() + "Z",
        "alerts": {"above": None, "below": None},
    }
    items.append(item)
    save_watchlist(items)
    print(f"✅ Added: {item['label']} ({mint[:8]}...)")
    return item


def remove_item(mint: str) -> bool:
    """Remove token from watchlist."""
    items = load_watchlist()
    filtered = [i for i in items if i["mint"] != mint and i["mint"].startswith(mint) is False]
    if len(filtered) == len(items):
        print(f"❌ {mint} tidak ada di watchlist")
        return False
    save_watchlist(filtered)
    print(f"✅ Removed: {mint[:8]}...")
    return True


def update_item(mint: str, label: str = None, note: str = None,
                above: float = None, below: float = None) -> bool:
    """Update watchlist item."""
    items = load_watchlist()
    for i in items:
        if i["mint"] == mint or i["mint"].startswith(mint):
            if label: i["label"] = label
            if note: i["note"] = note
            if above is not None: i["alerts"]["above"] = above
            if below is not None: i["alerts"]["below"] = below
            i["updated_at"] = datetime.utcnow().isoformat() + "Z"
            save_watchlist(items)
            print(f"✅ Updated: {i['label']}")
            return True
    print(f"❌ {mint} tidak ditemukan")
    return False


def list_items():
    """Print watchlist."""
    items = load_watchlist()
    if not items:
        print("📭 Watchlist kosong. Tambah dengan: watchlist_manager.py add <MINT>")
        return
    print(f"\n⭐ Watchlist ({len(items)} token):\n")
    print(f"  {'#':<4} {'LABEL':<14} {'MINT':<14} {'NOTE':<30} {'ALERTS':<20}")
    print(f"  {'─'*4} {'─'*14} {'─'*14} {'─'*30} {'─'*20}")
    for idx, i in enumerate(items, 1):
        alerts = []
        if i.get("alerts", {}).get("above"): alerts.append(f"↑${i['alerts']['above']}")
        if i.get("alerts", {}).get("below"): alerts.append(f"↓${i['alerts']['below']}")
        alert_str = " ".join(alerts) or "-"
        print(f"  {idx:<4} {i['label'][:14]:<14} {i['mint'][:12]:<14} {i['note'][:30]:<30} {alert_str:<20}")
    print(f"\n💾 File: {WATCHLIST_FILE}\n")


def clear_watchlist():
    """Clear all items (with confirm)."""
    items = load_watchlist()
    if not items:
        print("📭 Already empty")
        return
    confirm = input(f"⚠️  Hapus {len(items)} item? Ketik 'yes' untuk konfirmasi: ")
    if confirm == "yes":
        save_watchlist([])
        print("✅ Cleared")
    else:
        print("❌ Cancelled")


def main():
    parser = argparse.ArgumentParser(description="Watchlist manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # add
    p_add = sub.add_parser("add", help="Add token to watchlist")
    p_add.add_argument("mint")
    p_add.add_argument("--label", help="Display label")
    p_add.add_argument("--note", help="Personal note")
    p_add.add_argument("--tags", nargs="+", help="Tags (e.g. trending meme)")

    # remove
    p_rm = sub.add_parser("remove", help="Remove token")
    p_rm.add_argument("mint")

    # update
    p_up = sub.add_parser("update", help="Update item")
    p_up.add_argument("mint")
    p_up.add_argument("--label")
    p_up.add_argument("--note")
    p_up.add_argument("--above", type=float, help="Alert above this price")
    p_up.add_argument("--below", type=float, help="Alert below this price")

    # list
    sub.add_parser("list", help="Show all items")

    # clear
    sub.add_parser("clear", help="Clear all (with confirm)")

    args = parser.parse_args()

    if args.cmd == "add":
        add_item(args.mint, args.label or "", args.note or "", args.tags or [])
    elif args.cmd == "remove":
        remove_item(args.mint)
    elif args.cmd == "update":
        update_item(args.mint, args.label, args.note, args.above, args.above if args.above else None, args.below)
    elif args.cmd == "list":
        list_items()
    elif args.cmd == "clear":
        clear_watchlist()


if __name__ == "__main__":
    main()
