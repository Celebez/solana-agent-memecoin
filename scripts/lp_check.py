#!/usr/bin/env python3
"""
🌊 lp_check.py — Cek LP Baru di DexScreener

Ambil pair Solana baru yang muncul di DexScreener, filter by likuiditas
minimum dan durasi listing, print ke stdout (bisa di-pipe ke alert).

Usage:
    python lp_check.py [--min-liquidity 5000] [--max-age-hours 24]

Dependencies:
    pip install requests
"""
import argparse
import time
import requests
from datetime import datetime, timezone

DEXSCREENER_LATEST = "https://api.dexscreener.com/latest/dex/pairs/solana"


def fetch_pairs(min_liq: float, max_age_hours: int):
    """Fetch new Solana pairs from DexScreener (search-based)."""
    # DexScreener tidak punya endpoint 'newest' langsung — kita search trending.
    try:
        resp = requests.get(DEXSCREENER_LATEST, timeout=20)
        resp.raise_for_status()
        pairs = resp.json().get("pairs", [])
    except Exception as e:
        print(f"❌ DexScreener error: {e}")
        return []

    now = time.time()
    filtered = []
    for p in pairs:
        liq = float((p.get("liquidity") or {}).get("usd") or 0)
        if liq < min_liq:
            continue
        created_ms = p.get("pairCreatedAt") or 0
        age_hours = (now * 1000 - created_ms) / (1000 * 3600)
        if age_hours > max_age_hours:
            continue

        filtered.append({
            "token": (p.get("baseToken") or {}).get("address", "?"),
            "symbol": (p.get("baseToken") or {}).get("symbol", "?"),
            "name": (p.get("baseToken") or {}).get("name", "?"),
            "liquidity_usd": liq,
            "volume_24h": float((p.get("volume") or {}).get("h24") or 0),
            "market_cap": float(p.get("marketCap") or 0),
            "price_change_24h": float(p.get("priceChange", {}).get("h24") or 0),
            "age_hours": round(age_hours, 1),
            "url": p.get("url", ""),
            "dex": p.get("dexId", "?"),
        })

    return sorted(filtered, key=lambda x: x["age_hours"])


def main():
    parser = argparse.ArgumentParser(description="Cek LP baru Solana di DexScreener")
    parser.add_argument("--min-liquidity", type=float, default=5000,
                        help="Minimum liquidity USD (default: 5000)")
    parser.add_argument("--max-age-hours", type=int, default=24,
                        help="Max age pair dalam jam (default: 24)")
    parser.add_argument("--limit", type=int, default=20, help="Max pairs to show")
    args = parser.parse_args()

    print(f"\n🌊 LP Baru Solana")
    print(f"   Min liquidity: ${args.min_liquidity:,.0f}")
    print(f"   Max age: {args.max_age_hours}h\n")

    pairs = fetch_pairs(args.min_liq, args.max_age_hours)
    if not pairs:
        print("📭 Tidak ada LP baru yang match criteria.")
        return

    print(f"{'SYMBOL':<12} {'LIQ':>10} {'VOL 24h':>12} {'AGE':>8}  URL")
    print("-" * 90)
    for p in pairs[:args.limit]:
        print(f"{p['symbol'][:12]:<12} ${p['liquidity_usd']:>9,.0f} ${p['volume_24h']:>11,.0f} {p['age_hours']:>7.1f}h  {p['url']}")

    print(f"\n📊 Total: {len(pairs)} pair baru")
    print(f"\n⚠️  SELALU jalankan check_token.py sebelum buy!\n")


if __name__ == "__main__":
    main()
