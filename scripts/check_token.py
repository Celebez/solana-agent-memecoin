#!/usr/bin/env python3
"""
🛡️ check_token.py — Token Safety Check via Helius RPC

Cek mint authority, freeze authority, supply, dan top holders untuk
token Solana. Output color-coded dengan composite rug score.

Usage:
    export HELIUS_API_KEY="your-key-here"
    python check_token.py <MINT_ADDRESS>

Dependencies:
    pip install requests
"""
import os
import sys
import json
import requests
from typing import Optional, Dict, List, Tuple

# ============================================================
# Konfigurasi
# ============================================================
HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
DEXSCREENER_API = "https://api.dexscreener.com/latest/dex"
HELIUS_RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"


def color_status(ok: bool, msg: str) -> str:
    """Format status dengan warna hijau/merah."""
    icon = "✅" if ok else "🚨"
    color = GREEN if ok else RED
    return f"{color}{icon} {msg}{RESET}"


def color_warning(msg: str) -> str:
    return f"{YELLOW}⚠️  {msg}{RESET}"


def rpc_call(method: str, params: list) -> Optional[Dict]:
    """Call Helius RPC JSON-RPC endpoint."""
    if not HELIUS_API_KEY:
        print(f"{RED}❌ HELIUS_API_KEY tidak di-set!{RESET}")
        print(f"   Export: export HELIUS_API_KEY='your-key-here'")
        print(f"   Daftar gratis: https://dashboard.helius.dev")
        sys.exit(1)

    payload = {"jsonrpc": "2.0", "id": "helius-check", "method": method, "params": params}

    try:
        resp = requests.post(HELIUS_RPC_URL, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            print(f"{RED}❌ RPC Error: {data['error']}{RESET}")
            return None
        return data.get("result")
    except requests.exceptions.RequestException as e:
        print(f"{RED}❌ Network error: {e}{RESET}")
        return None


def check_mint_info(mint: str) -> Tuple[bool, bool, int, int]:
    """
    Cek mint & freeze authority.

    Returns:
        (mint_authority_null, freeze_authority_null, supply, decimals)
    """
    result = rpc_call("getAccountInfo", [mint, {"encoding": "jsonParsed"}])
    if not result or not result.get("value"):
        return (False, False, 0, 0)

    parsed = result["value"]["data"]["parsed"]["info"]
    mint_auth = parsed.get("mintAuthority")
    freeze_auth = parsed.get("freezeAuthority")
    supply = int(parsed.get("supply", 0))
    decimals = int(parsed.get("decimals", 0))

    mint_null = mint_auth is None
    freeze_null = freeze_auth is None

    return (mint_null, freeze_null, supply, decimals)


def check_top_holders(mint: str, limit: int = 10) -> Tuple[float, List[Dict]]:
    """
    Cek top N holders via getTokenLargestAccounts.

    Returns:
        (top_n_percentage, list_of_holders)
    """
    result = rpc_call("getTokenLargestAccounts", [mint])
    if not result or not result.get("value"):
        return (0.0, [])

    accounts = result["value"]
    total_ui = sum(float(a.get("uiAmount") or 0) for a in accounts)

    if total_ui == 0:
        return (0.0, accounts)

    top_n_ui = sum(float(a.get("uiAmount") or 0) for a in accounts[:limit])
    percentage = (top_n_ui / total_ui) * 100

    return (round(percentage, 2), accounts[:limit])


def check_dexscreener(mint: str) -> Dict:
    """Cek LP, volume, market cap via DexScreener (free, no key)."""
    try:
        resp = requests.get(f"{DEXSCREENER_API}/tokens/{mint}", timeout=15)
        resp.raise_for_status()
        data = resp.json()
        pairs = data.get("pairs") or []
        if not pairs:
            return {}

        # Pair dengan likuiditas tertinggi
        pair = max(pairs, key=lambda p: float((p.get("liquidity") or {}).get("usd") or 0))

        return {
            "price_usd": float(pair.get("priceUsd") or 0),
            "market_cap": float(pair.get("marketCap") or 0),
            "fdv": float(pair.get("fdv") or 0),
            "liquidity_usd": float((pair.get("liquidity") or {}).get("usd") or 0),
            "volume_24h": float((pair.get("volume") or {}).get("h24") or 0),
            "price_change_24h": float(pair.get("priceChange", {}).get("h24") or 0),
            "dex": pair.get("dexId"),
            "pair_url": pair.get("url"),
        }
    except Exception as e:
        print(f"{YELLOW}⚠️  DexScreener error: {e}{RESET}")
        return {}


def calculate_rug_score(mint_null: bool, freeze_null: bool, holders_pct: float,
                        liquidity_usd: float, volume_24h: float) -> Tuple[int, str]:
    """
    Composite rug score (0–100).

    Returns:
        (score, verdict_label)
    """
    score = 0
    if mint_null: score += 25
    if freeze_null: score += 20
    if holders_pct < 40: score += 20
    elif holders_pct < 60: score += 10
    if liquidity_usd > 50_000: score += 15
    elif liquidity_usd > 10_000: score += 8
    if volume_24h > 10_000: score += 10
    elif volume_24h > 1_000: score += 5
    score += 10  # bonus for completing all checks

    if score >= 80: return (score, "🟢 SANGAT AMAN")
    if score >= 60: return (score, "🟢 AMAN (DYOR)")
    if score >= 40: return (score, "🟡 RISIKO SEDANG")
    if score >= 20: return (score, "🟠 RISIKO TINGGI")
    return (score, "🔴 JANGAN BUY")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <MINT_ADDRESS>")
        print(f"Example: python check_token.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU")
        sys.exit(1)

    mint = sys.argv[1].strip()

    print(f"\n{BOLD}{BLUE}🔍 Checking token: {mint}{RESET}\n")

    # 1. Mint info
    mint_null, freeze_null, supply, decimals = check_mint_info(mint)
    if supply == 0:
        print(f"{RED}❌ Token tidak ditemukan atau invalid{RESET}")
        sys.exit(1)

    supply_display = supply / (10 ** decimals) if decimals else supply
    print(f"{BLUE}Mint Info:{RESET}")
    print(f"  {color_status(mint_null, 'Mint Authority    : ' + ('None (AMAN)' if mint_null else 'AKTIF (BAHAYA!)'))}")
    print(f"  {color_status(freeze_null, 'Freeze Authority  : ' + ('None (AMAN)' if freeze_null else 'AKTIF (BAHAYA!)'))}")
    print(f"  {BLUE}ℹ️  Total Supply     : {supply_display:,.0f} ({decimals} decimals){RESET}\n")

    # 2. Top holders
    holders_pct, top_holders = check_top_holders(mint)
    if holders_pct > 0:
        if holders_pct < 40:
            status = color_status(True, f"Top 10 Holders    : {holders_pct}% (AMAN)")
        elif holders_pct < 60:
            status = color_warning(f"Top 10 Holders    : {holders_pct}% (SEDANG)")
        else:
            status = color_status(False, f"Top 10 Holders    : {holders_pct}% (BAHAYA!)")
        print(f"{BLUE}Holder Distribution:{RESET}")
        print(f"  {status}")
        for i, h in enumerate(top_holders[:5], 1):
            addr = h.get("address", "?")[:8] + "..."
            amount = float(h.get("uiAmount") or 0)
            print(f"     #{i} {addr}  {amount:,.0f}")
        print()

    # 3. DexScreener
    dex_data = check_dexscreener(mint)
    liquidity_usd = volume_24h = 0.0

    if dex_data:
        print(f"{BLUE}Market Data (DexScreener):{RESET}")
        if dex_data.get("price_usd"):
            print(f"  💵 Price         : ${dex_data['price_usd']:.8f}")
        if dex_data.get("market_cap"):
            print(f"  📊 Market Cap    : ${dex_data['market_cap']:,.0f}")
        if dex_data.get("liquidity_usd"):
            liquidity_usd = dex_data["liquidity_usd"]
            liq_status = "AMAN" if liquidity_usd > 50_000 else "SEDANG" if liquidity_usd > 10_000 else "BAHAYA"
            liq_color = GREEN if liquidity_usd > 50_000 else YELLOW if liquidity_usd > 10_000 else RED
            print(f"  💧 Liquidity     : {liq_color}${liquidity_usd:,.0f} ({liq_status}){RESET}")
        if dex_data.get("volume_24h"):
            volume_24h = dex_data["volume_24h"]
            print(f"  📈 Volume 24h    : ${volume_24h:,.0f}")
        if dex_data.get("dex"):
            print(f"  🌐 DEX           : {dex_data['dex']}")
        if dex_data.get("pair_url"):
            print(f"  🔗 Chart         : {dex_data['pair_url']}")
        print()
    else:
        print(f"{YELLOW}⚠️  Tidak ada data DexScreener (mungkin token belum listing){RESET}\n")

    # 4. Composite score
    score, verdict = calculate_rug_score(mint_null, freeze_null, holders_pct, liquidity_usd, volume_24h)

    print(f"{BOLD}{'='*50}{RESET}")
    print(f"{BOLD}📊 RUG SCORE: {score}/100  →  {verdict}{RESET}")
    print(f"{BOLD}{'='*50}{RESET}\n")

    if score < 60:
        print(f"{RED}⛔ TIDAK DISARANKAN untuk dibeli. Cari token lain.{RESET}")
    elif score < 80:
        print(f"{YELLOW}⚠️  DYOR lebih lanjut. Cek Twitter, Telegram, dev wallet.{RESET}")
    else:
        print(f"{GREEN}✅ Token terlihat aman. Tetap pakai position sizing & stop loss!{RESET}")

    print()


if __name__ == "__main__":
    main()
