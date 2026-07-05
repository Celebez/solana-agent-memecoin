#!/usr/bin/env python3
"""
📊 rug_score.py — Composite Rug Scoring untuk Token Solana

Kombinasikan multiple signal jadi 1 score (0–100).
Bisa standalone atau dipanggil dari script lain.

Usage:
    from rug_score import score_token
    result = score_token("7xKXtg...")
    print(result["verdict"])
"""
import os
import sys
import requests
from typing import Dict

HELIUS_API_KEY = os.environ.get("HELIUS_API_KEY")
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
DEXSCREENER = "https://api.dexscreener.com/latest/dex"


def _rpc(method: str, params: list) -> dict:
    payload = {"jsonrpc": "2.0", "id": "score", "method": method, "params": params}
    try:
        r = requests.post(HELIUS_RPC, json=payload, timeout=10)
        r.raise_for_status()
        return r.json().get("result") or {}
    except Exception:
        return {}


def _dex(mint: str) -> dict:
    try:
        r = requests.get(f"{DEXSCREENER}/tokens/{mint}", timeout=10)
        pairs = r.json().get("pairs") or []
        return pairs[0] if pairs else {}
    except Exception:
        return {}


def score_token(mint: str) -> Dict:
    """
    Return dict with: score (0-100), verdict, breakdown, details.
    """
    breakdown = {}
    details = {}

    # Mint info
    info = _rpc("getAccountInfo", [mint, {"encoding": "jsonParsed"}])
    parsed = (info.get("value") or {}).get("data", {}).get("parsed", {}).get("info", {}) if info else {}

    mint_null = parsed.get("mintAuthority") is None
    freeze_null = parsed.get("freezeAuthority") is None
    breakdown["mint_authority_null"] = 25 if mint_null else 0
    breakdown["freeze_authority_null"] = 20 if freeze_null else 0
    details["supply"] = int(parsed.get("supply", 0))

    # Top holders
    holders = _rpc("getTokenLargestAccounts", [mint])
    accounts = (holders.get("value") or []) if holders else []
    total = sum(float(a.get("uiAmount") or 0) for a in accounts)
    top10 = sum(float(a.get("uiAmount") or 0) for a in accounts[:10])
    pct = (top10 / total * 100) if total > 0 else 100
    if pct < 40:
        breakdown["top10_holders"] = 20
    elif pct < 60:
        breakdown["top10_holders"] = 10
    else:
        breakdown["top10_holders"] = 0
    details["top10_pct"] = round(pct, 2)

    # DexScreener
    pair = _dex(mint)
    liq = float((pair.get("liquidity") or {}).get("usd") or 0)
    vol = float((pair.get("volume") or {}).get("h24") or 0)
    if liq > 50_000:
        breakdown["liquidity"] = 15
    elif liq > 10_000:
        breakdown["liquidity"] = 8
    else:
        breakdown["liquidity"] = 0
    if vol > 10_000:
        breakdown["volume"] = 10
    elif vol > 1_000:
        breakdown["volume"] = 5
    else:
        breakdown["volume"] = 0
    breakdown["bonus"] = 10  # bonus for full check
    details["liquidity_usd"] = liq
    details["volume_24h"] = vol

    score = sum(breakdown.values())

    if score >= 80:
        verdict = "🟢 SANGAT AMAN"
    elif score >= 60:
        verdict = "🟢 AMAN (DYOR)"
    elif score >= 40:
        verdict = "🟡 RISIKO SEDANG"
    elif score >= 20:
        verdict = "🟠 RISIKO TINGGI"
    else:
        verdict = "🔴 JANGAN BUY"

    return {"mint": mint, "score": score, "verdict": verdict,
            "breakdown": breakdown, "details": details}


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <MINT>")
        sys.exit(1)
    if not HELIUS_API_KEY:
        print("❌ HELIUS_API_KEY required")
        sys.exit(1)

    result = score_token(sys.argv[1])
    print(f"\n📊 Score: {result['score']}/100 → {result['verdict']}\n")
    print("Breakdown:")
    for k, v in result["breakdown"].items():
        print(f"  {k:<25} +{v}")
    print(f"\nDetails:")
    for k, v in result["details"].items():
        print(f"  {k:<20} {v}")


if __name__ == "__main__":
    main()
